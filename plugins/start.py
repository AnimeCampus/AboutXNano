import asyncio
from datetime import datetime
from time import time
from bot import Bot
from config import ADMINS, CHANNEL_ID
from database.sql import add_user, full_userbase, query_msg
from pyrogram import filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from pyrogram.types import InlineKeyboardMarkup, Message
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from helper_func import decode, get_messages


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60**2 * 24),
    ("hour", 60**2),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)

@Bot.on_message(filters.command("send"))
async def handle_send_command(client, message):
    try:
        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name

        # Check if the command has a message following it
        if len(message.command) > 1:
            # Check if the message contains a reply to an image
            if message.reply_to_message and message.reply_to_message.photo:
                # Get the file ID of the image
                file_id = message.reply_to_message.photo[-1].file_id
                # Download the image
                image_path = await client.download_media(file_id)
                # Send the image to the database channel
                caption = f"@GenXNano You Have Photo From\n\n{username}\n(ID: {user.id})"
                await client.send_photo(CHANNEL_ID, photo=image_path, caption=caption)
                await message.reply("Your photo has been sent to the database channel.")
            else:
                text = " ".join(message.command[1])
                # Send the extracted text to the database channel
                await client.send_message(CHANNEL_ID, f"@GenXNano You Have Message From\n\n{username}\n(ID: {user.id}):\n```{text}```")
                await message.reply("Your message has been sent to the database channel.")
        else:
            await message.reply("Please provide a message to send with the /send command.")
    except Exception as e:
        LOGGER(__name__).warning(e)




        
@Bot.on_message(filters.command("ans") & filters.user(ADMINS))
async def answer_user(client, message):
    try:
        # Check if the command has the necessary arguments
        if len(message.command) < 3:
            await message.reply("Usage: /ans user_id message")
            return

        user_id = int(message.command[1])
        text = " ".join(message.command[2:])

        # Send the reply to the specified user
        await client.send_message(user_id, text)
        await message.reply(f"Your message has been sent to user with ID {user_id}.")
    except Exception as e:
        LOGGER(__name__).warning(e)
        

@Bot.on_message(filters.command("start"))
async def start_command(client: Bot, message: Message):
    id = message.from_user.id
    user_name = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else None
    )

    try:
        await add_user(id, user_name)
    except:
        pass  # This will catch exceptions and do nothing

    # Send a welcome message to the user
    await message.reply(
        "👋 <b>Welcome to About Nano Bot</b> 🤖\n\n"
        "Use the buttons below to explore the features:",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("About", callback_data="about"),
                ],
                [
                    InlineKeyboardButton("Help", callback_data="help"),
                    InlineKeyboardButton("Channel", url="https://t.me/AboutXNano"),
                ],
                [
                    InlineKeyboardButton("Close", callback_data="close")
                ],
            ]
        ),
    )

    # Send a message to the database channel about the new user
    try:
        username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        user_id = message.from_user.id
        await client.send_message(CHANNEL_ID, f"#NewUser:\n{username}\n(ID: {user_id})")
    except Exception as e:
        LOGGER(__name__).warning(e)




@Bot.on_message(filters.command(["users", "stats"]) & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(
        chat_id=message.chat.id, text="<code>Processing ...</code>"
    )
    users = await full_userbase()
    await msg.edit(f"{len(users)} <b>Users use this bot</b>")


@Bot.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await query_msg()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply(
            "<code>Broadcasting Message...</code>"
        )
        for row in query:
            chat_id = int(row[0])
            if chat_id not in ADMINS:
                try:
                    await broadcast_msg.copy(chat_id, protect_content=PROTECT_CONTENT)
                    successful += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await broadcast_msg.copy(chat_id, protect_content=PROTECT_CONTENT)
                    successful += 1
                except UserIsBlocked:
                    blocked += 1
                except InputUserDeactivated:
                    deleted += 1
                except BaseException:
                    unsuccessful += 1
                total += 1
        status = f"""<b><u>Successful Broadcast</u>
───────────────────────
 Number of Users: <code>{total}</code>
 Success: <code>{successful}</code>
 Failed: <code>{unsuccessful}</code>
 User blocked: <code>{blocked}</code>
 Deleted Account: <code>{deleted}</code></b>"""
        return await pls_wait.edit(status)
    else:
        msg = await message.reply(
            "<code>Use this command must be replay to the telegram message that you want to broadcast.</code>"
        )
        await asyncio.sleep(8)
        await msg.delete()


@Bot.on_message(filters.command("ping"))
async def ping_pong(client, m: Message):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    m_reply = await m.reply_text("Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "<b>PONG!!</b>🏓 \n"
        f"<b>• Pinger -</b> <code>{delta_ping * 1000:.3f}ms</code>\n"
        f"<b>• Uptime -</b> <code>{uptime}</code>\n"
    )


@Bot.on_message(filters.command("uptime"))
async def get_uptime(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 <b>Bot Status:</b>\n"
        f"• <b>Uptime:</b> <code>{uptime}</code>\n"
        f"• <b>Start Time:</b> <code>{START_TIME_ISO}</code>"
    )
