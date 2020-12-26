from pyrogram import filters
from helper import Helper


@Helper.on_message(filters.command("start") & filters.private)
def resources_command(client, message):
    message.reply(f"Samahani huyu Bot ni wa @python_eafrica.\nSifanyi chochote hapa")