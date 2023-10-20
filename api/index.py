import os

from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__)

app.secret_key = b"UGRjnwb/KIjlYQkGfhATAah9WvOuSxYZcG/UuskC6xV9KCICQGiLGt4w/YbEkNWk"
# OAuth2 must make use of HTTPS in production environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 1163564558191972482    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "zycFaWl8eZaaNPsKu2u7pI3LzW3AH3lp"                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "https://discord-oa-uth-test.vercel.app/callback"# URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = "MTE2MzU2NDU1ODE5MTk3MjQ4Mg.G8t0V0.Eqv_l6Xlm3FX1kIurUS_BNC1oumAUNrnAyh4rk"# Required to access BOT resources.


discord = DiscordOAuth2Session(app)

def welcome_user(user):
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )

@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback/")
def callback():
    discord.callback()
    user = discord.fetch_user()
    welcome_user(user)
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""