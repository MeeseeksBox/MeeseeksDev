"""
Meeseeksbox main app module
"""
import base64
import os
import signal

from .commands import close, help_make, merge, migrate_issue_request
from .commands import open as _open
from .commands import ready
from .meeseeksbox.commands import (
    black_suggest,
    blackify,
    debug,
    party,
    precommit,
    replyuser,
    safe_backport,
    say,
    tag,
    untag,
    zen,
)
from .meeseeksbox.core import Config, MeeseeksBox

org_allowlist = [
    "MeeseeksBox",
    "Jupyter",
    "IPython",
    "JupyterLab",
    "jupyter-server",
    "jupyter-widgets",
    "voila-dashboards",
    "jupyter-xeus",
    "Carreau",
    "matplotlib",
    "scikit-learn",
    "pandas-dev",
    "scikit-image",
]

usr_denylist: list = []

usr_allowlist = [
    "Carreau",
    "gnestor",
    "ivanov",
    "fperez",
    "mpacer",
    "minrk",
    "takluyver",
    "sylvaincorlay",
    "ellisonbg",
    "blink1073",
    "damianavila",
    "jdfreder",
    "rgbkrk",
    "tacaswell",
    "willingc",
    "jhamrick",
    "lgpage",
    "jasongrout",
    "ian-r-rose",
    "kevin-bates",
    # matplotlib people
    "tacaswell",
    "QuLogic",
    "anntzer",
    "NelleV",
    "dstansby",
    "efiring",
    "choldgraf",
    "dstansby",
    "dopplershift",
    "jklymak",
    "weathergod",
    "timhoffm",
    # pandas-dev
    "jreback",
    "jorisvandenbossche",
    "gfyoung",
    "TomAugspurger",
]

# https://github.com/integrations/meeseeksdev/installations/new
# already ? https://github.com/organizations/MeeseeksBox/settings/installations/4268
# https://github.com/integration/meeseeksdev


def load_config_from_env():
    """
    Load the configuration, for now stored in the environment
    """
    config: dict = {}

    integration_id_str = os.environ.get("GITHUB_INTEGRATION_ID")
    botname = os.environ.get("GITHUB_BOT_NAME", None)

    if not integration_id_str:
        raise ValueError("Please set GITHUB_INTEGRATION_ID")

    if not botname:
        raise ValueError("Need to set a botname")
    if "@" in botname:
        print("Don't include @ in the botname !")

    botname = botname.replace("@", "")
    at_botname = "@" + botname
    integration_id = int(integration_id_str)

    if "B64KEY" in os.environ:
        config["key"] = base64.b64decode(bytes(os.environ["B64KEY"], "ASCII"))
    elif "TESTING" not in os.environ:
        raise ValueError("Missing B64KEY environment variable")
    config["botname"] = botname
    config["at_botname"] = at_botname
    config["integration_id"] = integration_id
    config["webhook_secret"] = os.environ.get("WEBHOOK_SECRET")
    config["port"] = int(os.environ.get("PORT", 5000))
    # config option to forward requests as-is to a test server.
    config["forward_staging_url"] = os.environ.get("FORWARD_STAGING_URL", "")
    print("saw config forward", config["forward_staging_url"])

    # Despite their names, this are not __your__ account, but an account created
    # for some functionalities of mr-meeseeks. Indeed, github does not allow
    # cross repositories pull-requests with Applications, so I use a personal
    # account just for that.
    config["personal_account_name"] = os.environ.get("PERSONAL_ACCOUNT_NAME")
    config["personal_account_token"] = os.environ.get("PERSONAL_ACCOUNT_TOKEN")

    return Config(**config).validate()


green = "\x1b[0;32m"
yellow = "\x1b[0;33m"
blue = "\x1b[0;34m"
red = "\x1b[0;31m"
normal = "\x1b[0m"


def main():
    print(blue + "====== (re) starting ======" + normal)
    config = load_config_from_env()

    app_v = os.environ.get("HEROKU_RELEASE_VERSION", None)
    if app_v:
        import keen

        try:
            keen.add_event("deploy", {"version": int(app_v[1:])})
        except Exception as e:
            print(e)
    config.org_allowlist = org_allowlist + [o.lower() for o in org_allowlist]
    config.user_allowlist = usr_allowlist + [u.lower() for u in usr_allowlist]
    config.user_denylist = usr_denylist + [u.lower() for u in usr_denylist]
    commands = {
        "hello": replyuser,
        "zen": zen,
        "backport": safe_backport,
        "safe_backport": safe_backport,
        "migrate": migrate_issue_request,
        "tag": tag,
        "untag": untag,
        "open": _open,
        "close": close,
        "autopep8": blackify,
        "reformat": blackify,
        "black": blackify,
        "blackify": blackify,
        "suggestions": black_suggest,
        "pre-commit": precommit,
        "precommit": precommit,
        "ready": ready,
        "merge": merge,
        "say": say,
        "debug": debug,
        "party": party,
    }
    commands["help"] = help_make(commands)
    box = MeeseeksBox(commands=commands, config=config)

    signal.signal(signal.SIGTERM, box.sig_handler)
    signal.signal(signal.SIGINT, box.sig_handler)

    box.start()


if __name__ == "__main__":
    main()
