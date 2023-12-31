import os

from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__)

app.secret_key = b"UGRjnwb/KIjlYQkGfhATAah9WvOuSxYZcG/UuskC6xV9KCICQGiLGt4w/YbEkNWk"
# OAuth2 must make use of HTTPS in production environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 1163564558191972482    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")           # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "https://discord-oauth-testing.vercel.app/callback"# URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN") # Required to access BOT resources.


discord = DiscordOAuth2Session(app)

def welcome_user(user):
    user.add_to_guild(1158574703368220732)
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )

@app.route("/login/")
def login():
    return discord.create_session(scope=["guilds", "guilds.join", "guilds.members.read"])


@app.route("/callback/")
def callback():
    try:
        discord.callback()
        user = discord.fetch_user()
        welcome_user(user)
        return redirect(url_for(".roles"))
    except Exception as ex:
        return str(ex)

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.errorhandler(Exception)
def oh_no_error(e):
    return str(e)

@app.route("/me/")
@requires_authorization
def me():

    user = discord.fetch_user()
    try:
        welcome_user(user)
    except Exception as ex:
        return str(ex)
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""

@app.route("/roles/")
@requires_authorization
def roles():
    # user = discord.fetch_user()
    guild_id = 1158574703368220732
    result = discord.request(f"/users/@me/guilds/{guild_id}/member")
    return result