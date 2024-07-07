from MahakMusic import app
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest
from typing import Union, Optional
from os import environ
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops
from asyncio import sleep
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from MahakMusic.utils.blaze import admin_filter
from unidecode import unidecode
import os


LOGGER = getLogger(__name__)

class LeftDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_left(self, chat_id):
        self.data[chat_id] = {"state": "off"}  # Default state is "off"

    async def rm_left(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]

left = LeftDatabase()

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None


EVAA = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/sitaramusicbot?startgroup=true"),
    ],
]

# --------------------------------------------------------------------------------- #

get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)

# --------------------------------------------------------------------------------- #

async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],
    profile_path: Optional[str] = None
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((286, 286))
        bg.paste(resized, (297, 117), resized)


    img_draw = ImageDraw.Draw(bg)

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path


# --------------------------------------------------------------------------------- #

bg_path = "MahakMusic/assets/CUTELEF.jpg"
font_path = "MahakMusic/assets/SwanseaBold-D0ox.ttf"

# --------------------------------------------------------------------------------- #


#command handler
@app.on_message(filters.command("left") & ~filters.private)
async def auto_state(_, message):
    usage = "**Usage:**\n⦿/left [on|off]\n➤sɪᴛᴀʀᴀ sᴘᴇᴄɪᴀʟ ʟᴇғᴛ.........."
    if len(message.command) == 1:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        A = await left.find_one(chat_id)
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "off":
            if A:
                await message.reply_text("**ʟᴇғᴛ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ !**")
            else:
                await left.add_left(chat_id)
                await message.reply_text(f"**ᴅɪsᴀʙʟᴇᴅ ʟᴇғᴛ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ** {message.chat.title}")
        elif state == "on":
            if not A:
                await message.reply_text("**ᴇɴᴀʙʟᴇ ʟᴇғᴛ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ.**")
            else:
                await left.rm_left(chat_id)
                await message.reply_text(f"**ᴇɴᴀʙʟᴇᴅ ʟᴇғᴛ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ ** {message.chat.title}")
        else:
            await message.reply_text(usage)
    else:
        await message.reply("**sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇɴᴀʙʟᴇ ʟᴇғᴛ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ!**")


@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client: app, member: ChatMemberUpdated):
#db source 
    chat_id = member.chat.id
    A = await left.find_one(chat_id)
    if A:
        return
         
    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {
            "banned", "left", "restricted"
        }
        and member.old_chat_member
    ):
        pass
    else:
        return

    user = (
        member.old_chat_member.user
        if member.old_chat_member
        else member.from_user
    )

    # Check if the user has a profile photo
    if user.photo and user.photo.big_file_id:
        try:
            # Add the photo path, caption, and button details
            photo = await app.download_media(user.photo.big_file_id)

            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )

            caption = f"ㅤㅤ  ㅤ◦•●◉✿ ᴜsᴇʀ ʟᴇғᴛ ✿◉●•◦\n▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰\n\n❖ ᴀ ᴍᴇᴍʙᴇʀ ʟᴇғᴛ ғʀᴏᴍ ɢʀᴏᴜᴘ.\n\n● ɢʀᴏᴜᴘ ➥ {member.chat.title}\n● ᴜsᴇʀ ɴᴀᴍᴇ ➥ {user.mention}\n● sᴇᴇ ʏᴏᴜ sᴏᴏɴ ᴀɢᴀɪɴ, ʙᴀʙʏ.\n\n❖ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ ๛ s ɪ ᴛ ᴀ ʀ ᴀ࿐\n▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰"
            
            # Send the message with the photo, caption, and button
            await client.send_photo(
                chat_id=member.chat.id,
                photo=welcome_photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(EVAA),)
        except RPCError as e:
            print(e)
            return
    else:
        # Handle the case where the user has no profile photo
        print(f"❖ User {user.id} has no profile photo.")
  
