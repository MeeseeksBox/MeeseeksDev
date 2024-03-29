# Contributing

## Test Deployment

- Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

You will need to have an account in Heroku.

Log in to Heroku:

```bash
heroku login
```

If creating, run:

```bash
heroku create meeseeksdev-$USER
```

Otherwise, run:

```bash
heroku git:remote -a meeseeksdev-$USER
```

Then run:

```bash
git push heroku $(git rev-parse --abbrev-ref HEAD):master
heroku open
```

To view the logs in a terminal window, use:

```bash
heroku logs --app meeseeksdev=$USER -t
```

### GitHub App Configuration

Create a GitHub App for testing on your account
Homepage URL: https://meeseeksdev-$USER.herokuapp.com/
Webhook URL: https://meeseeksdev-$USER.herokuapp.com/webhook
Webhook Secret: Set and store as WEBHOOK_SECRET env variable
Private Key: Generate and store as B64KEY env variable

Grant write access to content, issues, and users.
Subscribe to Issue and Issue Comment Events.

Install the application on your user account, at least in your MeeseeksDev fork.

### Heroku Configuration

You will need a Github token with access to cancel builds. This

This needs to be setup on the [Heroku Application settings](https://dashboard.heroku.com/apps/jupyterlab-bot/settings)

On the `Config Vars`. section set the following keys::

```
GITHUB_INTEGRATION_ID="<App ID of the Application>"
B64KEY="<B64 encoding of entire pem file>"
GITHUB_BOT_NAME="<meeseeksdev-$USER>"
WEBHOOK_SECRET="<value from the webhooks add above>"
PERSONAL_ACCOUNT_NAME="<account name>"
PERSONAL_ACCOUNT_TOKEN="<github personal access token with repo access>"
```

### Code Styling

`MeeseeksDev` has adopted automatic code formatting so you shouldn't
need to worry too much about your code style.
As long as your code is valid,
the pre-commit hook should take care of how it should look.
`pre-commit` and its associated hooks will automatically be installed when
you run `pip install -e ".[test]"`

To install `pre-commit` manually, run the following::

```shell
pip install pre-commit
pre-commit install
```

You can invoke the pre-commit hook by hand at any time with:

```shell
pre-commit run
```

which should run any autoformatting on your code
and tell you about any errors it couldn't fix automatically.
You may also install [black integration](https://github.com/psf/black#editor-integration)
into your text editor to format code automatically.

If you have already committed files before setting up the pre-commit
hook with `pre-commit install`, you can fix everything up using
`pre-commit run --all-files`. You need to make the fixing commit
yourself after that.

Some of the hooks only run on CI by default, but you can invoke them by
running with the `--hook-stage manual` argument.
