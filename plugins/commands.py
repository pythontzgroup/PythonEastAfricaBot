from pyrogram import filters, emoji
from pyrogram.types import (
    Message, ChatPermissions, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
)
from helper import Helper
import time
from functools import wraps
import asyncio

TARGET = Helper.CHATS
SAVIOURS = [731217828, 472424515]


async def reply_and_delete(message: Message, text: str):
    await message.delete()
    await message.reply(
        text,
        quote=False,
        reply_to_message_id=getattr(
            message.reply_to_message,
            "message_id", None
        ),
        disable_web_page_preview=True
    )


######################################################################################


def admins_only(func):
    @wraps(func)
    async def decorator(bot: Helper, message: Message):
        if bot.is_admin(message):
            await func(bot, message)

        await message.delete()

    decorator.admin = True

    return decorator


########################################################################################


@Helper.on_message(filters.command("ping", prefixes="#") & filters.chat(TARGET))
async def ping(_, message: Message):
    """Ping Hopertzbot"""
    start = time.time()
    reply = await message.reply_text("...")
    delta_ping = time.time() - start
    await reply.edit_text(f"**Pong!** `{delta_ping * 1000:.3f} ms`")


##################################################################################################


Elezea = """
Tafadhali, tupe **mfano mdogo** ili  tuweze kuelewa tatizo lako kwa urahisi 
[Ninawezaje kuunda mfano mdogo ?](https://stackoverflow.com/help/minimal-reproducible-example)
"""


@Helper.on_message(filters.command("eleza", prefixes="#") & filters.chat(TARGET))
async def ex(_, message: Message):
    """Ask for minimal example"""
    await reply_and_delete(message, Elezea)


################################################################################


ULIZA = """
Samahani, swali lako halijaundwa vizuri. Tafadhali, fuata miongozo katika kiungo hapa chini.
[Ninaulizaje swali zuri?](https://stackoverflow.com/help/how-to-ask)
"""


@Helper.on_message(filters.command("uliza", prefixes="#") & filters.chat(TARGET))
async def ask(_, message: Message):
    """Kuuliza Maswali"""
    await reply_and_delete(message, ULIZA)


############################################################################################


NJE = "Hoja hii imezimwa na haihusiani na Python"


@Helper.on_message(filters.command("nje", prefixes="#") & filters.chat(TARGET))
async def off(_, message: Message):
    """Nje ya mada"""
    answer = NJE
    await reply_and_delete(message, answer)


############################################################################################


MADINI = """
**Rasilimali nzuri za Python kwa ajili ya kujifunza **
• [Official Tutorial](https://docs.python.org/3/tutorial/index.html) - Book
• [Dive Into Python 3](https://www.diveinto.org/python3/table-of-contents.html) - Book
• [Hitchhiker's Guide!](https://docs.python-guide.org) - Book
• [Learn Python](https://www.learnpython.org/) - Interactive
• [Project Python](http://projectpython.net) - Interactive
• [Python Video Tutorials](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU) - Video
• [MIT OpenCourseWare](http://ocw.mit.edu/6-0001F16) - Course
• @PythonRes - Channel

"""


@Helper.on_message(filters.command("madini", prefixes="#") & filters.chat(TARGET))
async def rcs(_, message: Message):
    """Good Python resources"""
    await reply_and_delete(message, MADINI)


######################################################################################################


SHERIA = """
Kanuni za Kikundi:

1.Hiki ni kikundi cha Python. Majadiliano yote yanapaswa kuhusiana na Python.

2.Majadiliano ya lugha nyingine ni marufuku.

3.Yeyote atakayechapisha au kusambaza nyenzo zozote zinazohusiana na betting, skrill, dent, forex, sarafu za crypto nk zitaondolewa mara moja.

4.Kuomba programu, programu au vifaa vya utapeli ni marufuku isipokuwa swali linahusiana na Python.

5.Ikiwa unahitaji msaada na code yako, tuma screenshot.

6.Unaweza kutumia Kiingereza au Kiswahili katika kikundi hiki.

7.Kundi hili limekusudiwa kwa wale wanaojua au wanataka kujifunza Python.

8.Ikiwa unahitaji vifaa vya kujifunzia, tafuta kikundi kwa kutumia #resources

9.Maswali yote yanapaswa kuulizwa katika Kikundi. Hauruhusiwi kumfuata mtu inbox na kumuulliza..

10.Yeyote atakayekwenda kinyume na sheria zetu ataonywa au kuondolewa. Tunataka kutoa njia kwa watu kujifunza Python katika Afrika Mashariki.
"""


@Helper.on_message(filters.command("sheria", prefixes="#") & filters.chat(TARGET))
async def res(_, message: Message):
    """Good Python resources"""
    await reply_and_delete(message, SHERIA)


########################################################################################


NAKILI = """
Tuma code au traceback kutumia orodha tofauti zilizopendekezwa

- https://nekobin.com/
- https://del.dog
- https://dpaste.org
- https://linkode.org
- https://hastebin.com
- https://bin.kv2.dev
"""


@Helper.on_message(filters.command("nakili", prefixes="#") & filters.chat(TARGET))
async def paste(_, message: Message):
    await reply_and_delete(message, NAKILI)


#################################################################################################


SOMA = "Tafadhali, soma nyaraka za python: https://docs.python.org"


@Helper.on_message(filters.command("soma", prefixes="#") & filters.chat(TARGET))
async def rtd(_, message: Message):
    await reply_and_delete(message, SOMA)


###############################################################################################

text_bot = f"Mimi ni bot {emoji.ROBOT}. Epuka spamming. "


@Helper.on_message(filters.command("beep", prefixes="#") & filters.chat(TARGET))
@admins_only
async def i_am(_, message: Message):
    await reply_and_delete(message, text_bot)


####################################################################################
MESSAGE_DATE_DIFF = 86400


@Helper.on_message(filters.command("futa", prefixes="#") & filters.chat(TARGET))
@admins_only
async def delete(bot: Helper, message: Message):
    """Delete messages"""
    reply = message.reply_to_message

    if not reply:
        return

    # Don't delete admins messages
    if bot.is_admin(reply):
        m = await message.reply("Samahani, sifuti ujumbe wa wasimamizi.")
        await asyncio.sleep(5)
        await m.delete()
        return

    # Don't delete messages that are too old
    if message.date - reply.date > MESSAGE_DATE_DIFF:
        m = await message.reply("Samahani, sifuti ujumbe ambao ni wa zamani sana.")
        await asyncio.sleep(5)
        await m.delete()
        return

    cmd = message.command

    # No args, delete the mentioned message alone
    if len(cmd) == 1:
        await reply.delete()
        return


#################################################################################################
@Helper.on_callback_query(filters.regex(r"^(?P<action>unban)\.(?P<uid>\d+)"))
async def unban(bot: Helper, query: CallbackQuery):
    action, user_id = query.data.split(".")
    user_id = int(user_id)
    text = query.message.text

    if action == "unban":
        if query.from_user.id not in SAVIOURS:
            await query.answer("Hopertz/JustMojo tu wanaweza kuwakomboa", show_alert=True)
            return

    await bot.restrict_chat_member(
        query.message.chat.id,
        user_id,
        ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_stickers=True,
            can_send_animations=True,
            can_send_games=True,
            can_use_inline_bots=True,
            can_add_web_page_previews=True,
            can_send_polls=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True
        )
    )

    await query.edit_message_text(f"~~{text.markdown}~~\n\nUmekombolewa (umesamehewa)")


@Helper.on_message(filters.command("fukuza", prefixes="#") & filters.chat(TARGET))
@admins_only
async def ban(bot: Helper, message: Message):
    """Ban a user in chat"""
    reply = message.reply_to_message

    if not reply:
        return

    # Don't ban admins
    if bot.is_admin(reply):
        m = await message.reply("Sifukuzi wasimamizi")
        await asyncio.sleep(5)
        await m.delete()
        return

    await bot.restrict_chat_member(message.chat.id, reply.from_user.id, ChatPermissions())

    await message.reply(
        f"__Umemzuia {reply.from_user.mention} moja kwa moja__",
        quote=False,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Mkomboe", f"unban.{reply.from_user.id}")
        ]])
    )


######################################################################################
HELP = f"""
Orodha ya amri zilizopo

• #ping - Ping command
. #beep* - Ujumbe wa bot
• #eleza - Uliza kutumia mfano mdogo
• #nje - mazungumzo ya nje ya mada
• #uliza - Jinsi ya kuuliza maswali
• #madini - Rasilimali nzuri za Python
• #nakili - kubandika mtandaoni
• #sheria - Sheria za kikundi
• #soma - Soma nyaraka za python
• #futa* - Futa ujumbe
• #fukuza* - Piga marufuku mtumiaji
• #onesha - Onyesha ujumbe huu

* Wasimamizi tu
"""


@Helper.on_message(filters.command("onesha", prefixes="#") & filters.chat(TARGET))
async def helping(_, message: Message):
    """Show this message"""
    await reply_and_delete(message, HELP)
