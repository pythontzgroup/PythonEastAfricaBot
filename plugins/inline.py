from helper import Helper
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent
)
from pyrogram.errors import BadRequest

SAVIOURS = [731217828, 472424515]

my_id_filter = filters.create(lambda _, query: query.from_user.id in SAVIOURS)


@Helper.on_inline_query(my_id_filter)
async def answer(client, query):
    string = query

    if string:
        try:
            await string.answer(
                results=[InlineQueryResultArticle(title="bonyeza",
                                                  input_message_content=InputTextMessageContent(
                                                      f"{string.query}"))])
        except BadRequest:
            pass
    else:
        pass
