import asyncio, os, json, logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice, PreCheckoutQuery,
)
from deep_translator import GoogleTranslator


logging.basicConfig(level=logging.INFO)


BOT_TOKEN = "8950076192:AAEClrKXqiyyG2ju9hOhFyd_zUfr4fEmF60"
ADMIN_ID = 8813054628
CHANNEL_ID = "@WorlldStudios"
CHANNEL_URL = "https://t.me/WorlldStudios"
FREE_URL = "https://t.me/FreeeWorlld"
USERS_DB = "users.json"
WORLDS_DB = "worlds.json"
CHITS_DB = "chits.json"


bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


TEXTS = {
"ru": {
"choose_lang": "🌍 <b>Выбери язык</b>",
"menu": "🏠 <b>Главное меню</b>",
"btn_check": "📢 Проверить подписку",
"btn_worlds": "🔐 Приватные миры",
"btn_chits": "🔓 Приватные читы",
"btn_settings": "⚙️ Настройки",
"sub_need": "❌ <b>Сначала подпишись на канал.</b>\n\nПосле подписки нажми «Проверить подписку».",
"sub_ok": "✅ <b>Подписка подтверждена.</b>\n\nДобро пожаловать!",
"sub_btn": "📢 Подписаться",
"worlds_hdr": "🔐 <b>Приватные миры</b>\n\nВыбери мир:",
"buy_hdr": "💎 <b>Приобрести мир можно за</b>",
"btn_buy": "⭐ Купить за {price} звёзд",
"btn_free": "🎁 Бесплатно",
"paid_ok": "✅ <b>Спасибо за покупку!</b>",
"settings_hdr": "⚙️ <b>Настройки</b>\n\nТекущий язык: Русский 🇷🇺",
"btn_chlang": "🌐 Сменить язык",
"btn_back": "⬅️ Назад",
"btn_continue": "🎞️ Продолжить",
"no_worlds": "Пока нет миров.",
"world_not_found": "⚠️ <b>Мир не найден.</b>",
"sending_file": "📥 Отправляю твой мир...",
"file_caption": "🎮 <b>Твой мир Minecraft</b>\n\nПриятной игры!",
"chits_hdr": "🔓 <b>Приватные читы</b>\n\nВыбери раздел:",
"no_chits": "Пока нет разделов.",
"btn_download": "📥 Скачать",
},
"en": {
"choose_lang": "🌍 <b>Choose your language</b>",
"menu": "🏠 <b>Main menu</b>",
"btn_check": "📢 Check subscription",
"btn_worlds": "🔐 Private worlds",
"btn_chits": "🔓 Private cheats",
"btn_settings": "⚙️ Settings",
"sub_need": "❌ <b>Subscribe first.</b>\n\nAfter subscribing, press «Check subscription».",
"sub_ok": "✅ <b>Subscription confirmed.</b>",
"sub_btn": "📢 Subscribe",
"worlds_hdr": "🔐 <b>Private worlds</b>\n\nChoose a world:",
"buy_hdr": "💎 <b>Get this world for</b>",
"btn_buy": "⭐ Buy for {price} stars",
"btn_free": "🎁 Free",
"paid_ok": "✅ <b>Thank you for purchase!</b>",
"settings_hdr": "⚙️ <b>Settings</b>\n\nCurrent language: English 🇬🇧",
"btn_chlang": "🌐 Change language",
"btn_back": "⬅️ Back",
"btn_continue": "🎞️ Continue",
"no_worlds": "No worlds yet.",
"world_not_found": "⚠️ <b>World not found.</b>",
"sending_file": "📥 Sending your world...",
"file_caption": "🎮 <b>Your Minecraft world</b>\n\nEnjoy!",
"chits_hdr": "🔓 <b>Private cheats</b>\n\nChoose a section:",
"no_chits": "No sections yet.",
"btn_download": "📥 Download",
},
"hi": {
"choose_lang": "🌍 <b>अपनी भाषा चुनें</b>",
"menu": "🏠 <b>मुख्य मेनू</b>",
"btn_check": "📢 सब्सक्रिप्शन जांचें",
"btn_worlds": "🔐 निजी दुनिया",
"btn_chits": "🔓 निजी चीट्स",
"btn_settings": "⚙️ सेटिंग्स",
"sub_need": "❌ <b>पहले सब्सक्राइब करें।</b>",
"sub_ok": "✅ <b>सब्सक्रिप्शन की पुष्टि हो गई।</b>",
"sub_btn": "📢 सब्सक्राइब करें",
"worlds_hdr": "🔐 <b>निजी दुनिया</b>",
"buy_hdr": "💎 <b>यह दुनिया प्राप्त करें</b>",
"btn_buy": "⭐ {price} सितारों के लिए खरीदें",
"btn_free": "🎁 मुफ़्त",
"paid_ok": "✅ <b>खरीदारी के लिए धन्यवाद!</b>",
"settings_hdr": "⚙️ <b>सेटिंग्स</b>",
"btn_chlang": "🌐 भाषा बदलें",
"btn_back": "⬅️ वापस",
"btn_continue": "🎞️ जारी रखें",
"no_worlds": "अभी कोई दुनिया नहीं।",
"world_not_found": "⚠️ <b>दुनिया नहीं मिली।</b>",
"sending_file": "📥 आपकी दुनिया भेजी जा रही है...",
"file_caption": "🎮 <b>आपकी Minecraft दुनिया</b>",
"chits_hdr": "🔓 <b>निजी चीट्स</b>",
"no_chits": "अभी कोई सेक्शन नहीं।",
"btn_download": "📥 डाउनलोड",
},
}


def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass


users = load_json(USERS_DB)
worlds = load_json(WORLDS_DB)
chits = load_json(CHITS_DB)


_free_worlds = {}


def load_free_worlds():
    try:
        with open("free_worlds.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


_free_worlds = load_free_worlds()


def save_free_worlds():
    try:
        with open("free_worlds.json", "w", encoding="utf-8") as f:
            json.dump(_free_worlds, f, ensure_ascii=False, indent=2)
    except:
        pass


_translate_cache = {}


def translate(text, target):
    if not text:
        return ""
    if target == "ru":
        return text
    key = f"{target}:{text[:50]}"
    if key in _translate_cache:
        return _translate_cache[key]
    try:
        result = GoogleTranslator(source="ru", target=target).translate(text)
        _translate_cache[key] = result
        return result
    except:
        return text


def t(uid, key, **kw):
    lang = users.get(str(uid), "ru")
    txt = TEXTS[lang].get(key, TEXTS["ru"][key])
    return txt.format(**kw) if kw else txt


def tdesc(uid, text):
    return translate(text, users.get(str(uid), "ru"))


def set_user_lang(uid, lang):
    users[str(uid)] = lang
    save_json(USERS_DB, users)


def get_lang(uid):
    return users.get(str(uid))


async def is_subbed(uid):
    try:
        m = await bot.get_chat_member(CHANNEL_ID, uid)
        return m.status in ("creator", "administrator", "member")
    except:
        return False
def kb_lang():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="lang:hi")],
    ])


def kb_menu(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_check"), callback_data="check")],
        [InlineKeyboardButton(text=t(uid, "btn_worlds"), callback_data="worlds")],
        [InlineKeyboardButton(text=t(uid, "btn_chits"), callback_data="chits")],
        [InlineKeyboardButton(text=t(uid, "btn_settings"), callback_data="settings")],
    ])


def kb_sub(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "sub_btn"), url=CHANNEL_URL)],
        [InlineKeyboardButton(text=t(uid, "btn_check"), callback_data="check")],
    ])


def kb_worlds(uid):
    rows = []
    for code, w in worlds.items():
        rows.append([InlineKeyboardButton(text=w.get("name", code), callback_data=f"world:{code}")])
    rows.append([InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="back_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_buy(uid, code):
    w = worlds.get(code, {})
    price = w.get("price", 25)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_buy", price=price), callback_data=f"buy:{code}")],
        [InlineKeyboardButton(text=t(uid, "btn_free"), url=FREE_URL)],
        [InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="worlds")],
    ])


def kb_settings(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_chlang"), callback_data="chlang")],
        [InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="back_menu")],
    ])


def kb_chlang(uid):
    cur = get_lang(uid) or "ru"
    names = {"ru": "🇷🇺 Русский", "en": "🇬🇧 English", "hi": "🇮🇳 हिन्दी"}
    rows = []
    for code in ["ru", "en", "hi"]:
        mark = "✅ " if code == cur else ""
        rows.append([InlineKeyboardButton(text=mark + names[code], callback_data="lang:" + code)])
    rows.append([InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="settings")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_chits(uid):
    rows = []
    for sec in chits.keys():
        rows.append([InlineKeyboardButton(text=sec, callback_data=f"sec:{sec}")])
    rows.append([InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="back_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_softs(uid, sec):
    rows = []
    for soft in chits.get(sec, {}).keys():
        rows.append([InlineKeyboardButton(text=soft, callback_data=f"soft:{sec}:{soft}")])
    rows.append([InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="chits")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_soft_view(uid, sec, soft):
    s = chits.get(sec, {}).get(soft, {})
    link = s.get("link", "")
    rows = []
    if link:
        rows.append([InlineKeyboardButton(text=t(uid, "btn_download"), url=link)])
    rows.append([InlineKeyboardButton(text=t(uid, "btn_back"), callback_data=f"sec:{sec}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


@dp.callback_query(F.data == "back_menu")
async def cb_back_menu(call: CallbackQuery):
    uid = call.from_user.id
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
    else:
        await call.message.edit_text(t(uid, "menu"), reply_markup=kb_menu(uid))
    await call.answer()


@dp.callback_query(F.data == "check")
async def cb_check(call: CallbackQuery):
    uid = call.from_user.id
    if await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_ok"), reply_markup=kb_menu(uid))
    else:
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
    await call.answer()


@dp.callback_query(F.data == "settings")
async def cb_settings(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(t(uid, "settings_hdr"), reply_markup=kb_settings(uid))
    await call.answer()


@dp.callback_query(F.data == "chlang")
async def cb_chlang(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(t(uid, "choose_lang"), reply_markup=kb_chlang(uid))
    await call.answer()


@dp.callback_query(F.data.startswith("lang:"))
async def cb_lang(call: CallbackQuery):
    uid = call.from_user.id
    lang = call.data.split(":")[1]
    set_user_lang(uid, lang)
    if await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_ok"), reply_markup=kb_menu(uid))
    else:
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
    await call.answer()


@dp.callback_query(F.data == "worlds")
async def cb_worlds(call: CallbackQuery):
    uid = call.from_user.id
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    if not worlds:
        await call.message.edit_text(t(uid, "no_worlds"), reply_markup=kb_menu(uid))
        await call.answer()
        return
    await call.message.edit_text(t(uid, "worlds_hdr"), reply_markup=kb_worlds(uid))
    await call.answer()


@dp.callback_query(F.data.startswith("world:"))
async def cb_world(call: CallbackQuery):
    uid = call.from_user.id
    code = call.data.split(":", 1)[1]
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    w = worlds.get(code)
    if not w:
        await call.answer("Мир не найден", show_alert=True)
        return
    await call.answer()
    await call.message.delete()
    if w.get("video"):
        try:
            await bot.send_video(uid, w["video"])
        except:
            pass
    if w.get("photo"):
        try:
            await bot.send_photo(uid, w["photo"])
        except:
            pass
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_continue"), callback_data=f"cont:{code}")],
    ])
    await bot.send_message(uid, w.get("name", code), reply_markup=kb)


@dp.callback_query(F.data.startswith("cont:"))
async def cb_continue(call: CallbackQuery):
    uid = call.from_user.id
    code = call.data.split(":", 1)[1]
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    await call.message.edit_text(t(uid, "buy_hdr"), reply_markup=kb_buy(uid, code))
    await call.answer()


@dp.callback_query(F.data.startswith("buy:"))
async def cb_buy(call: CallbackQuery):
    uid = call.from_user.id
    code = call.data.split(":", 1)[1]
    w = worlds.get(code)
    if not w:
        await call.answer("Мир не найден", show_alert=True)
        return
    price = w.get("price", 25)
    await bot.send_invoice(
        chat_id=uid,
        title=w.get("name", code),
        description=f"Мир {w.get('name', code)} — {price} звёзд",
        payload=f"world:{code}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=w.get("name", code), amount=price)],
    )
    await call.answer()


@dp.pre_checkout_query()
async def pre_checkout(pcq: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pcq.id, ok=True)


@dp.message(F.successful_payment)
async def on_paid(msg: Message):
    uid = msg.from_user.id
    payload = msg.successful_payment.invoice_payload
    code = payload.split(":", 1)[1] if ":" in payload else payload
    w = worlds.get(code, {})
    await msg.answer(t(uid, "paid_ok"))
    username = msg.from_user.username or msg.from_user.first_name
    try:
        await bot.send_message(
            ADMIN_ID,
            f"💰 <b>Покупка!</b>\n\nМир: <b>{w.get('name', code)}</b> (код {code})\nПокупатель: @{username} (id {uid})"
        )
    except:
        pass


@dp.callback_query(F.data == "chits")
async def cb_chits(call: CallbackQuery):
    uid = call.from_user.id
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    if not chits:
        await call.message.edit_text(t(uid, "no_chits"), reply_markup=kb_menu(uid))
        await call.answer()
        return
    await call.message.edit_text(t(uid, "chits_hdr"), reply_markup=kb_chits(uid))
    await call.answer()


@dp.callback_query(F.data.startswith("sec:"))
async def cb_sec(call: CallbackQuery):
    uid = call.from_user.id
    sec = call.data.split(":", 1)[1]
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    if not chits.get(sec):
        await call.answer("Раздел пуст", show_alert=True)
        return
    await call.message.edit_text(f"🎮 <b>{sec}</b>", reply_markup=kb_softs(uid, sec))
    await call.answer()


@dp.callback_query(F.data.startswith("soft:"))
async def cb_soft(call: CallbackQuery):
    uid = call.from_user.id
    parts = call.data.split(":", 2)
    if len(parts) < 3:
        await call.answer()
        return
    _, sec, soft = parts
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    s = chits.get(sec, {}).get(soft)
    if not s:
        await call.answer("Софт не найден", show_alert=True)
        return
    await call.answer()
    await call.message.delete()
    desc = tdesc(uid, s.get("desc", ""))
    caption = f"<b>{soft}</b>\n\n{desc}"
    if s.get("photo"):
        try:
            await bot.send_photo(uid, s["photo"], caption=caption, reply_markup=kb_soft_view(uid, sec, soft))
            return
        except:
            pass
    await bot.send_message(uid, caption, reply_markup=kb_soft_view(uid, sec, soft))
# ==== СТАРТОВЫЙ ОБРАБОТЧИК: ловит /start и ?start=КОД ====


@dp.message(F.text.startswith("/start"))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    args = msg.text.split(maxsplit=1)
    param = args[1].strip() if len(args) > 1 else None


    if not get_lang(uid):
        if param:
            _pending_world[uid] = param
        await msg.answer(TEXTS["ru"]["choose_lang"], reply_markup=kb_lang())
        return


    if param:
        await send_world(uid, param)
        return


    if not await is_subbed(uid):
        await msg.answer(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        return
    await msg.answer(t(uid, "menu"), reply_markup=kb_menu(uid))


_pending_world = {}


async def send_world(uid, code):
    if not await is_subbed(uid):
        await bot.send_message(uid, t(uid, "sub_need"), reply_markup=kb_sub(uid))
        return
    if code in _free_worlds:
        await bot.send_message(uid, t(uid, "sending_file"))
        try:
            await bot.send_document(uid, _free_worlds[code], caption=t(uid, "file_caption"))
        except Exception as e:
            await bot.send_message(uid, t(uid, "world_not_found"))
        return
    if code in worlds:
        w = worlds[code]
        if w.get("video"):
            try:
                await bot.send_video(uid, w["video"])
            except:
                pass
        if w.get("photo"):
            try:
                await bot.send_photo(uid, w["photo"])
            except:
                pass
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t(uid, "btn_continue"), callback_data=f"cont:{code}")],
        ])
        await bot.send_message(uid, w.get("name", code), reply_markup=kb)
        return
    await bot.send_message(uid, t(uid, "world_not_found"))


# ==== АДМИН-КОМАНДЫ ====


@dp.message(F.document)
async def catch_file(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    fid = msg.document.file_id
    name = msg.document.file_name or "file"
    key = name.replace(".mcworld", "").strip().lower()
    if key.startswith("world"):
        _free_worlds[key] = fid
        save_free_worlds()
    else:
        worlds[key] = {"name": name.replace(".mcworld", ""), "price": 25, "video": None, "photo": None, "file": fid}
        save_json(WORLDS_DB, worlds)
    await msg.answer(f"✅ Сохранил мир: <b>{key}</b>\n\n<code>{fid}</code>")


@dp.message(F.text.startswith("/addworld"))
async def admin_addworld(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.replace("/addworld", "").strip().split("|")
        name = parts[0].strip()
        code = parts[1].strip()
        price = int(parts[2].strip())
        worlds[code] = {"name": name, "price": price, "video": None, "photo": None, "file": None}
        save_json(WORLDS_DB, worlds)
        await msg.answer(f"✅ Мир добавлен: <b>{name}</b> (код {code}, {price} ⭐)")
    except Exception as e:
        await msg.answer(f"❌ Формат: /addworld Название | КОД | 25\n{e}")


@dp.message(F.text.startswith("/setvideo"))
async def admin_setvideo(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    if not msg.reply_to_message or not msg.reply_to_message.video:
        await msg.answer("Ответь этой командой на видео.")
        return
    code = msg.text.replace("/setvideo", "").strip()
    if code in worlds:
        worlds[code]["video"] = msg.reply_to_message.video.file_id
        save_json(WORLDS_DB, worlds)
        await msg.answer(f"✅ Видео привязано к {code}")
    else:
        await msg.answer(f"Мир {code} не найден.")


@dp.message(F.text.startswith("/setphoto"))
async def admin_setphoto(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    if not msg.reply_to_message or not msg.reply_to_message.photo:
        await msg.answer("Ответь этой командой на фото.")
        return
    code = msg.text.replace("/setphoto", "").strip()
    if code in worlds:
        worlds[code]["photo"] = msg.reply_to_message.photo[-1].file_id
        save_json(WORLDS_DB, worlds)
        await msg.answer(f"✅ Фото привязано к миру {code}")
        return
    for sec in chits:
        if code in chits[sec]:
            chits[sec][code]["photo"] = msg.reply_to_message.photo[-1].file_id
            save_json(CHITS_DB, chits)
            await msg.answer(f"✅ Фото привязано к софту {code}")
            return
    await msg.answer(f"Мир/софт {code} не найден.")


@dp.message(F.text == "/listworlds")
async def admin_listworlds(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    lines = ["📋 <b>Платные миры:</b>"]
    if not worlds:
        lines.append("Нет.")
    for code, w in worlds.items():
        v = "🎥" if w.get("video") else "—"
        p = "🖼" if w.get("photo") else "—"
        f = "📄" if w.get("file") else "—"
        lines.append(f"• <b>{w.get('name')}</b> | {code} | {w.get('price')} ⭐ | видео {v} | фото {p} | файл {f}")
    lines.append(f"\n📋 <b>Бесплатные миры:</b> {len(_free_worlds)} шт.")
    for code in list(_free_worlds.keys())[:10]:
        lines.append(f"• {code}")
    if len(_free_worlds) > 10:
        lines.append(f"... и ещё {len(_free_worlds) - 10}")
    await msg.answer("\n".join(lines))


@dp.message(F.text.startswith("/delworld"))
async def admin_delworld(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    code = msg.text.replace("/delworld", "").strip()
    if code in worlds:
        del worlds[code]
        save_json(WORLDS_DB, worlds)
        await msg.answer(f"🗑 Мир {code} удалён.")
    elif code in _free_worlds:
        del _free_worlds[code]
        save_free_worlds()
        await msg.answer(f"🗑 Бесплатный мир {code} удалён.")
    else:
        await msg.answer(f"Мир {code} не найден.")


@dp.message(F.text.startswith("/setprice"))
async def admin_setprice(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.replace("/setprice", "").strip().split()
        code, price = parts[0], int(parts[1])
        if code in worlds:
            worlds[code]["price"] = price
            save_json(WORLDS_DB, worlds)
            await msg.answer(f"✅ {code} → {price} ⭐")
        else:
            await msg.answer(f"Мир {code} не найден.")
    except Exception as e:
        await msg.answer(f"Формат: /setprice CODE 25\n{e}")


@dp.message(F.text.startswith("/addsection"))
async def admin_addsection(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    sec = msg.text.replace("/addsection", "").strip()
    if not sec:
        await msg.answer("Формат: /addsection PUBG")
        return
    if sec not in chits:
        chits[sec] = {}
        save_json(CHITS_DB, chits)
        await msg.answer(f"✅ Раздел добавлен: <b>{sec}</b>")
    else:
        await msg.answer(f"Раздел {sec} уже есть.")


@dp.message(F.text.startswith("/addsoft"))
async def admin_addsoft(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.replace("/addsoft", "").strip().split("|")
        sec = parts[0].strip()
        soft = parts[1].strip()
        if sec not in chits:
            chits[sec] = {}
        chits[sec][soft] = {"desc": "", "link": "", "photo": None}
        save_json(CHITS_DB, chits)
        await msg.answer(f"✅ Софт <b>{soft}</b> добавлен в <b>{sec}</b>")
    except Exception as e:
        await msg.answer(f"Формат: /addsoft Standoff 2 | PlutoniumCrack\n{e}")


@dp.message(F.text.startswith("/setdesc"))
async def admin_setdesc(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.replace("/setdesc", "").strip().split("|", 1)
        soft = parts[0].strip()
        desc = parts[1].strip()
        for sec in chits:
            if soft in chits[sec]:
                chits[sec][soft]["desc"] = desc
                save_json(CHITS_DB, chits)
                await msg.answer(f"✅ Описание добавлено для {soft}")
                return
        await msg.answer(f"Софт {soft} не найден.")
    except Exception as e:
        await msg.answer(f"Формат: /setdesc PlutoniumCrack | Описание\n{e}")


@dp.message(F.text.startswith("/setlink"))
async def admin_setlink(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.replace("/setlink", "").strip().split("|", 1)
        soft = parts[0].strip()
        link = parts[1].strip()
        for sec in chits:
            if soft in chits[sec]:
                chits[sec][soft]["link"] = link
                save_json(CHITS_DB, chits)
                await msg.answer(f"✅ Ссылка добавлена для {soft}")
                return
        await msg.answer(f"Софт {soft} не найден.")
    except Exception as e:
        await msg.answer(f"Формат: /setlink PlutoniumCrack | https://drive.google.com/...\n{e}")


@dp.message(F.text == "/listsofts")
async def admin_listsofts(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    if not chits:
        await msg.answer("Разделов нет.")
        return
    lines = ["📋 <b>Читы:</b>"]
    for sec, softs in chits.items():
        lines.append(f"\n<b>{sec}</b>:")
        for name, s in softs.items():
            d = "✅" if s.get("desc") else "—"
            l = "✅" if s.get("link") else "—"
            p = "🖼" if s.get("photo") else "—"
            lines.append(f"  • {name} | описание {d} | ссылка {l} | фото {p}")
    await msg.answer("\n".join(lines))


@dp.message(F.text.startswith("/delsection"))
async def admin_delsection(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    sec = msg.text.replace("/delsection", "").strip()
    if sec in chits:
        del chits[sec]
        save_json(CHITS_DB, chits)
        await msg.answer(f"🗑 Раздел {sec} удалён.")
    else:
        await msg.answer(f"Раздел {sec} не найден.")


@dp.message(F.text.startswith("/delsoft”))
async def admin_delsoft(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    soft = msg.text.replace("/delsoft", "").strip()
    for sec in chits:
        if soft in chits[sec]:
            del chits[sec][soft]
            save_json(CHITS_DB, chits)
            await msg.answer(f"🗑 Софт {soft} удалён.")
            return
    await msg.answer(f"Софт {soft} не найден.")


# ============ ЛЮБОЙ ТЕКСТ = МЕНЮ ============


@dp.message(F.text)
async def any_text(msg: Message):
    uid = msg.from_user.id
    if uid == ADMIN_ID and msg.text.startswith("/"):
        return
    if not get_lang(uid):
        await msg.answer(TEXTS["ru"]["choose_lang"], reply_markup=kb_lang())
        return
    if not await is_subbed(uid):
        await msg.answer(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        return
    await msg.answer(t(uid, "menu"), reply_markup=kb_menu(uid))


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
