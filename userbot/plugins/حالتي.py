import random
import re
import time
from datetime import datetime
from platform import python_version

from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from userbot import StartTime, catub, catversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "utils"


@catub.cat_cmd(
    pattern="^(الحالة|stats)$",
    command=("الحالة", plugin_category),
    info={
        "header": "للتحقق من حالة البوت هل هو نشط ام لا",
        "options": "لإظهار الوسائط في هذا cmd ، تحتاج إلى تعيين ALIVE_PIC مع ارتباط الوسائط ، احصل على هذا عن طريق الرد على الوسائط بواسطة (تلكراف)",
        "usage": [
            "الحالة",
            "alive",
        ],
    },
)
async def amireallyalive(event):
    "إظهار تفاصيل البوت وهل هو نشط ام لا"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await edit_or_reply(event, "**▾∮ جاري الفحص إنتظر من فضلك ... 🤖❗️**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    CAT_IMG = gvarstatus("ALIVE_PIC")
    cat_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    caption = cat_caption.format(
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        catver=catversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if CAT_IMG:
        CAT = [x for x in CAT_IMG.split()]
        PIC = random.choice(CAT)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**▾∮ خطأ في قيمة الوسائط ✘**\n\n**قم بتغيير الرابط عن طريق**`ضع فار`\n**لا يمكن الحصول على الوسائط من هذا الرابط : -** `{PIC}`",
            )
    else:
        await edit_or_reply(
            event,
            caption,
        )


temp = "\n**▾∮ يعمل بوت Cat العربي بنجاح ✓\n\n**▾∮ قاعدة البيانات ↫** `{dbhealth}`\n**▾∮ اصدار التليثون ↫** `{telever}`\n**▾∮ اصدار Cat العربي ↫** `{catver}`\n**▾∮ اصدار بايثون ↫** `{pyver}`\n**▾∮ مدة التشغيل ↫** `{uptime}`\n**▾∮ المالك ↫** {mention}\n\n**⍣ⵧⵧⵧⵧⵧCat Arabicⵧⵧⵧⵧⵧ⍣**\n**▾∮** [𝓢𝓞𝓤𝓡𝓒𝓔 𝓒𝓐𝓣 😺](https://t.me/CatArabic)"


@catub.cat_cmd(
    pattern="^(حالتي|myself)$",
    command=("حالتي", plugin_category),
    info={
        "header": "للتحقق من حالة البوت هل هو نشط ام لا بوضع مضمن",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}ialive",
        ],
    },
)
# async def amireallyalive(event):
#    "A kind of showing bot details by your inline bot"
#    reply_to_id = await reply_id(event)
#    EMOJI = gvarstatus("ALIVE_EMOJI") or "▾∮"
#    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**▾∮ يعمل بوت Cat العربي بنجاح ✓**"
#    cat_caption = f"{ALIVE_TEXT}\n"
#    cat_caption += f"**{EMOJI} اصدار التليثون ↫** `{version.__version__}\n`"
#    cat_caption += f"**{EMOJI} اصدار Cat العربي ↫** `{catversion}`\n"
#    cat_caption += f"**{EMOJI} اصدار بايثون ↫** `{python_version()}\n`"
#    cat_caption += f"**{EMOJI} مالك التليثون ↫** {mention}\n"
#    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
#    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
#    await event.delete()


async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**Catuserbot is Up and Running**"
    cat_caption = f"{ALIVE_TEXT}\n"
    cat_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    cat_caption += f"**{EMOJI} Catuserbot Version :** `{catversion}`\n"
    cat_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    cat_caption += f"**{EMOJI} Master:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@catub.tgbot.on(CallbackQuery(data=re.compile(b"@BBSSS")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
