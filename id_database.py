import aiosqlite
import asyncio


async def connecting():
    async with aiosqlite.connect('id.db') as db:
        await db.execute("CREATE TABLE userid (user , status)")
        await db.commit()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connecting())
    loop.close()


if __name__ == '__main__':
    main()
