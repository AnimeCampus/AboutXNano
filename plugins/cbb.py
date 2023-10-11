# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

from bot import Bot
from config import OWNER, ADMINS
from Data import Data
from pyrogram import filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from pyrogram import Client, filters

@Bot.on_message(filters.private & filters.incoming & filters.command("about"))
async def _about(client: Bot, msg: Message):
    await client.send_message(
        msg.chat.id,
        Data.ABOUT.format(client.username, OWNER),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.mbuttons),
    )


@Bot.on_message(filters.private & filters.incoming & filters.command("help"))
async def _help(client: Bot, msg: Message):
    await client.send_message(
        msg.chat.id,
        "<b>💀💀<b>\n" + Data.HELP,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.buttons),
    )


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        try:
            await query.message.edit_text(
                text=Data.ABOUT.format(client.username, OWNER),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.mbuttons),
            )
        except MessageNotModified:
            pass
    elif data == "help":
        try:
            await query.message.edit_text(
                text="<b>💀💀</b>\n" + Data.HELP,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )
        except MessageNotModified:
            pass
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except BaseException:
            pass

@Bot.on_message(filters.command("sudolist") & filters.user(ADMINS))
async def su_list_command(client: Client, message: Message):
    users_list = ""
    for user_id in ADMINS:
        try:
            user = await client.get_users(user_id)
            users_list += f"{user.first_name} (@{user.username})\n"
        except Exception as e:
            # Handle any errors here
            users_list += f"User ID {user_id} - Error: {str(e)}\n"
    
    # Save the list to an admin.txt file
    with open("admin.txt", "w") as admin_file:
        admin_file.write(users_list)
    
    await message.reply(f"Admin Users:\n{users_list}")
    await client.send_document(chat_id=message.chat.id, document="admin.txt")


                     
