from pyrogram import client, emoji, filters
from captcha_emojis import em
from random import sample, shuffle
from pyrogram.types import Message, ChatPermissions
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from helper import Helper
import time
import aiosqlite


MENTION = "[{}](tg://user?id={})"
TARGET = Helper.CHATS
MESSAGE = "{}, Chagua emoji's unazoziona. Unaruhusiwa kukosea mara moja tu."


@Helper.on_message(filters.chat(TARGET) & filters.new_chat_members)
async def welcome(bot: Helper, message: Message):
    global captcha, start
    start = time.time()
    user_id = ",".join([str(i.id) for i in message.new_chat_members])
    user_id = int(user_id)
    db = await aiosqlite.connect('id.db')
    cursor = await db.execute('SELECT * FROM userid')
    rows = await cursor.fetchall()
    print(rows, 'first')
    for row in rows:
        if row[0] == user_id and row[1] == 'unsolved':
            await message.reply('Mara ya mwisho kujiunga, Hukujithibisha. Jaribu tena baada ya masaa 6')
            kick = await bot.kick_chat_member(message.chat.id, user_id, int(time.time() + 21600))
            await kick.delete()
            await db.execute("DELETE from userid where user = ?", (user_id,))
            await db.commit()
            return
    await db.execute("INSERT INTO userid VALUES (?,?)", (user_id, 'unsolved'))
    await db.commit()
    await cursor.close()
    await db.close()
    await bot.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
    new_members = [MENTION.format(i.first_name, i.id) for i in message.new_chat_members]
    text = MESSAGE.format(", ".join(new_members))
    captchas = [e for e in sample(em, 5)]
    list_emoji = [emoji.__getattribute__(e) for e in em if e not in captchas]
    list_emoji = sample(list_emoji, 10)
    captcha = [emoji.__getattribute__(e) for e in captchas]
    captcha_txt = "  ".join(captcha)
    list_emoji = list_emoji + captcha
    shuffle(list_emoji)

    t = await message.reply(
        f'{text} \n  {captcha_txt}',
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[0],
                        callback_data=f"{list_emoji[0]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[1],
                        callback_data=f"{list_emoji[1]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[2],
                        callback_data=f"{list_emoji[2]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[3],
                        callback_data=f"{list_emoji[3]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[4],
                        callback_data=f"{list_emoji[4]}.{user_id}"
                    ),
                ],
                [  # Second row
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[5],
                        callback_data=f"{list_emoji[5]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[6],
                        callback_data=f"{list_emoji[6]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[7],
                        callback_data=f"{list_emoji[7]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[8],
                        callback_data=f"{list_emoji[8]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[9],
                        callback_data=f"{list_emoji[9]}.{user_id}"
                    ),
                ],
                [  # third row
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[10],
                        callback_data=f"{list_emoji[10]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[11],
                        callback_data=f"{list_emoji[11]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[12],
                        callback_data=f"{list_emoji[12]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[13],
                        callback_data=f"{list_emoji[13]}.{user_id}"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        list_emoji[14],
                        callback_data=f"{list_emoji[14]}.{user_id}"
                    ),
                ],

            ]
        )
    )


solver = set()
mistake = False


@Helper.on_callback_query(~filters.regex(r"^(?P<action>unban)\.(?P<uid>\d+)"))
async def captchafunc(bot: Helper, query: CallbackQuery):
    global cnt, solver, mistake
    emoj, user_id = query.data.split(".")
    user_id = int(user_id)
    text = query.message.text

    if query.from_user.id != user_id:
        await query.answer("Samahani,huu ujumbe si wako.", show_alert=True)
        return

    if emoj in captcha:
        solver.add(emoj)
        if len(solver) == len(captcha):
            end = time.time()
            await query.edit_message_text(f"{emoji.STAR} Umefanikiwa,umetumia sekunde {round(end-start)}. Karibu East Africa Python Group")
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
            db = await aiosqlite.connect('id.db')
            cursor = await db.execute("UPDATE userid set status = ? where user = ?", ('solved', user_id))
            await db.commit()
            await cursor.close()
            await db.close()
            solver = set()
            mistake = False
            return
    elif mistake:
        res = await bot.kick_chat_member(query.message.chat.id, user_id, int(time.time() + 21600))
        await res.delete()
        mistake = False
        solver = set()
        await query.edit_message_text(f"Umeshindwa kujithibisha. Jaribu tena baada ya masaa 6")
        return

    elif emoj not in captcha:
        mistake = True


@Helper.on_message(filters.chat(TARGET) & filters.left_chat_member)
async def left_group(bot: Helper, message: Message):
    left_id = message.left_chat_member.id
    db = await aiosqlite.connect('id.db')
    cursor = await db.execute('SELECT * FROM userid')
    rows = await cursor.fetchall()
    print(rows, 'left')
    for row in rows:
        if left_id == row[0] and row[1] == 'solved':
            cursor = await db.execute("DELETE from userid where user = ?", (left_id,))
            await db.commit()

    await cursor.close()
    await db.close()
    await message.delete()
