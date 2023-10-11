import pyromod.listen
import sys

from pyrogram import Client

from config import (
    API_HASH,
    APP_ID,
    CHANNEL_ID,    
    LOGGER,
    OWNER,
    TG_BOT_TOKEN,
    TG_BOT_WORKERS,
)


class Bot(Client):
    def __init__(self):
        super().__init__(
            "Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    async def start(self):
        try:
            await super().start()
            bot_user = await self.get_me()
            self.username = bot_user.username
            self.bot_name = bot_user.first_name
            self.LOGGER(__name__).info(
                f"TG_BOT_TOKEN detected!\n┌ First Name: {self.bot_name}\n└ Username: @{self.username}\n——"
            )
        except Exception as error:
            self.LOGGER(__name__).warning(error)
            self.LOGGER(__name__).info("Bot stopped. Join the group https://t.me/SharingUserbot for assistance.")
            sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test_message = await self.send_message(chat_id=db_channel.id, text="Test Message", disable_notification=True)
            await test_message.delete()
            self.LOGGER(__name__).info(
                f"CHANNEL_ID Database detected!\n┌ Title: {db_channel.title}\n└ Chat ID: {db_channel.id}\n——"
            )
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Make sure @{self.username} is an admin in your database channel, Current CHANNEL_ID: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info("Bot stopped. Join the group https://t.me/SharingUserbot for assistance.")
            sys.exit()

        self.set_parse_mode("html")
        self.LOGGER(__name__).info(
            f"[🔥 SUCCESSFULLY ACTIVATED! 🔥]\n\nBOT Created by @{OWNER}\nIf @{OWNER} needs assistance, please ask in the group https://t.me/SharingUserbot"
        )

        # Send a deployment message to the specified database channel
        await self.send_message(chat_id=db_channel.id, text="Bot is fully deployed and active now!")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
