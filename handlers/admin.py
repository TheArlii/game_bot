from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from app.config import ADMIN_IDS
from keyboards.admin_menu import admin_main_menu
from utils.admin_check import is_admin
import json
import asyncio
import os

router = Router()

USERS_DB = "users.json"
LAVOZIM_DB = "data/lavozimlar.json"
SAVED_MESSAGES_DB = "data/admin_sent_messages.json"
PUSH_LOG = "data/push_log.json"

# ✅ Admin panel menyusi
@router.message(Command("panel"))
@router.message(F.text == "⚙️ Admin paneli")
async def show_admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("🛠 Admin paneliga xush kelibsiz!", reply_markup=admin_main_menu)

# ✅ Reklama xabarini yuborish
@router.message(F.text == "📩 Reklama yuborish")
async def reklama_yoriqnoma(message: Message):
    await message.answer(
        "✉️ Reklama yuborish uchun bu formatda yozing:\n\n"
        "<code>/reklama Sizning xabaringiz...</code>"
    )

@router.message(F.text.startswith("/reklama"))
async def send_reklama(message: Message, bot: Bot):
    if message.from_user.id not in ADMIN_IDS:
        return

    text = message.text.replace("/reklama", "").strip()
    if not text:
        await message.answer("❗ Reklama matni bo‘sh bo‘lmasin.")
        return

    if not os.path.exists(USERS_DB):
        await message.answer("❌ Foydalanuvchilar topilmadi.")
        return

    with open(USERS_DB, "r", encoding="utf-8") as f:
        users = json.load(f)

    sent_messages = []
    for user_id in users:
        try:
            msg = await bot.send_message(user_id, text)
            sent_messages.append({
                "user_id": user_id,
                "message_id": msg.message_id
            })
        except:
            continue

    with open(SAVED_MESSAGES_DB, "w", encoding="utf-8") as f:
        json.dump(sent_messages, f)

    await message.answer("✅ Reklama yuborildi. 24 soatdan keyin avtomatik o‘chiriladi.")

    # ⏰ 24 soatdan keyin xabarlarni o‘chirish
    await asyncio.sleep(86400)
    for item in sent_messages:
        try:
            await bot.delete_message(item["user_id"], item["message_id"])
        except:
            continue

# ✅ Push xabar yuborish (o‘chmaydi)
@router.message(F.text == "🚀 Push xabar yuborish")
async def push_yoriqnoma(message: Message):
    await message.answer(
        "🚀 Push xabar yuborish uchun bu formatda yozing:\n\n"
        "<code>/push Sizning xabaringiz...</code>"
    )

@router.message(F.text.startswith("/push"))
async def send_push(message: Message, bot: Bot):
    if message.from_user.id not in ADMIN_IDS:
        return

    text = message.text.replace("/push", "").strip()
    if not text:
        await message.answer("❗ Xabar matni bo‘sh bo‘lmasin.")
        return

    if not os.path.exists(USERS_DB):
        await message.answer("❌ Foydalanuvchilar topilmadi.")
        return

    with open(USERS_DB, "r", encoding="utf-8") as f:
        users = json.load(f)

    sent = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            sent += 1
        except:
            continue

    with open(PUSH_LOG, "w", encoding="utf-8") as f:
        json.dump(list(users.keys()), f)

    await message.answer(f"✅ Push xabar {sent} ta foydalanuvchiga yuborildi.")

# ✅ Statistika
@router.message(Command("stat"))
@router.message(F.text == "📊 Statistika")
async def show_statistics(message: Message):
    if not is_admin(message.from_user.id):
        return

    if not os.path.exists(USERS_DB):
        await message.answer("👥 0 ta foydalanuvchi ro‘yxatda.")
        return

    with open(USERS_DB, "r", encoding="utf-8") as f:
        users = json.load(f)

    count = len(users)
    await message.answer(f"👥 Botdan foydalanuvchilar soni: <b>{count}</b> ta")

# ✅ Lavozim berish
@router.message(F.text == "➕ Lavozim berish")
async def lavozim_yoriqnoma(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "➕ Lavozim berish uchun quyidagicha yozing:\n"
        "<code>/lavozim user_id lavozim_nomi</code>"
    )

@router.message(F.text.startswith("/lavozim"))
async def ber_lavozim(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split()
    if len(args) < 3:
        await message.answer("❗ To‘liq formatda yozing:\n<code>/lavozim 123456789 VIP</code>")
        return

    user_id = args[1]
    lavozim = " ".join(args[2:])

    try:
        if not os.path.exists(LAVOZIM_DB):
            with open(LAVOZIM_DB, "w", encoding="utf-8") as f:
                json.dump({}, f)

        with open(LAVOZIM_DB, "r", encoding="utf-8") as f:
            data = json.load(f)

        data[user_id] = lavozim

        with open(LAVOZIM_DB, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        await message.answer(
            f"✅ Foydalanuvchiga lavozim tayinlandi:\n"
            f"🆔 <code>{user_id}</code>\n🔖 Lavozim: <b>{lavozim}</b>"
        )
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")

# ✅ ID orqali qidirish
@router.message(F.text == "🔍 ID orqali foydalanuvchini izlash")
async def izlash_yoriqnoma(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("🔍 Qidirish uchun yozing:\n<code>/izla 123456789</code>")

@router.message(F.text.startswith("/izla"))
async def izla_user(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("❗ ID ni to‘liq kiriting:\n<code>/izla 123456789</code>")
        return

    user_id = args[1]

    if not os.path.exists(USERS_DB):
        await message.answer("❌ Foydalanuvchilar bazasi topilmadi.")
        return

    with open(USERS_DB, "r", encoding="utf-8") as f:
        users = json.load(f)

    if user_id in users:
        user = users[user_id]
        name = user.get("name", "Noma'lum")
        ball = user.get("points", 0)
        await message.answer(
            f"🔎 <b>Foydalanuvchi topildi:</b>\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"📛 Ism: {name}\n"
            f"💰 Ball: {ball}"
        )
    else:
        await message.answer("❗ Foydalanuvchi topilmadi.")
