from pyrogram import Client
from pyrogram.types import Message


class Helper(Client):
    CREATOR_ID = 731217828
    CHATS = [-1001450354167]

    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            name,
            workdir="."
        )
        self.admins = {
            chat: {Helper.CREATOR_ID}
            for chat in Helper.CHATS
        }

    async def start(self):
        await super().start()
        # Fetch current admins from chats
        for chat, admins in self.admins.items():
            async for admin in self.iter_chat_members(chat, filter="administrators"):
                admins.add(admin.user.id)

    async def stop(self, *args):
        await super().stop()

    def is_admin(self, message: Message) -> bool:
        user_id = message.from_user.id
        chat_id = message.chat.id

        return user_id in self.admins[chat_id]
