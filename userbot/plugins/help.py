from telethon import functions

from userbot import catub

from ..Config import Config
from ..core import CMD_INFO, GRP_INFO, PLG_INFO
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

cmdprefix = Config.COMMAND_HAND_LER

plugin_category = "tools"

hemojis = {
    "ملفات الادمن": "👮‍♂️",
    "ملفات البوت": "🤖",
    "ملفات المرح": "⛄️",
    "ملفات الميديا": "🎧",
    "الادوات": "🧰",
    "المرفقات": "🗂",
    "الاضافيات": "➕",
}


def get_key(val):
    for key, value in PLG_INFO.items():
        for cmd in value:
            if val == cmd:
                return key
    return None


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


async def cmdinfo(input_str, event, plugin=False):
    if input_str[0] == cmdprefix:
        input_str = input_str[1:]
    try:
        about = CMD_INFO[input_str]
    except KeyError:
        if plugin:
            await edit_delete(
                event,
                f"**▾∮ لا يوجد ملف أو أمر مثل ↫** `{input_str}`** في بوتك.**",
            )
            return None
        await edit_delete(event, f"**▾∮ لا يوجد أمر مثل ↫**`{input_str}`** في بوتك.**")
        return None
    except Exception as e:
        await edit_delete(event, f"**▾∮ هنالك خطأ ... تحقق ↻**\n`{e}`")
        return None
    outstr = f"**اسم الامر :** `{cmdprefix}{input_str}`\n"
    plugin = get_key(input_str)
    if plugin is not None:
        outstr += f"**اسم الملف 📁:** `{plugin}`\n"
        category = getkey(plugin)
        if category is not None:
            outstr += f"**▾∮ القسم 👨‍🏫 ↫** `{category}`\n\n"
    outstr += f"**المقدمة 📍 :**\n{about[0]}"
    return outstr


async def plugininfo(input_str, event, flag):
    try:
        cmds = PLG_INFO[input_str]
    except KeyError:
        outstr = await cmdinfo(input_str, event, plugin=True)
        return outstr
    except Exception as e:
        await edit_delete(event, f"**▾∮ هنالك خطأ ... تحقق ↻**\n`{e}`")
        return None
    if len(cmds) == 1 and (flag is None or (flag and flag != "-p")):
        outstr = await cmdinfo(cmds[0], event, plugin=False)
        return outstr
    outstr = f"**اسم الملف 📁 :**`{input_str}`\n"
    outstr += f"**الأوامر المتوفرة :** `{len(cmds)}`\n"
    category = getkey(input_str)
    if category is not None:
        outstr += f"**▾∮ القسم 👨‍🏫 ↫** `{category}`\n\n"
    for cmd in sorted(cmds):
        outstr += f"⍣  **الامر :** `{cmdprefix}{cmd}`\n"
        try:
            outstr += f"⍣  **معلومات :** `{CMD_INFO[cmd][1]}`\n\n"
        except IndexError:
            outstr += f"⍣  **معلومات :** `لا يوجد`\n\n"
    outstr += f"**👩‍💻 طريقة الاستخدام : ** `{cmdprefix}مساعدة <اسم الامر>`\
        \n**ملاحظة : **إذا كان اسم الأمر هو نفسه اسم الملف المساعد ، فاستخدم هذا الاسم `{cmdprefix}مساعدة <اسم الامر>`."
    return outstr


async def grpinfo():
    outstr = "**▾∮ المكونات الإضافية في NovemberBot هي :**\n\n"
    outstr += f"**👩‍💻 طريقة الاستخدام : ** `{cmdprefix}مساعدة <اسم الملف>`\n\n"
    category = [
        "ملفات الادمن",
        "ملفات البوت",
        "ملفات المرح",
        "ملفات الميديا",
        "الادوات",
        "المرفقات",
        "الاضافيات",
    ]
    for cat in category:
        plugins = GRP_INFO[cat]
        outstr += f"**{hemojis[cat]} {cat.title()} **({len(plugins)})\n"
        for plugin in plugins:
            outstr += f"`{plugin}`  "
        outstr += "\n\n"
    return outstr


async def cmdlist():
    outstr = "**▾∮القائمة الإجمالية للأوامر في NovemberBot هي :**\n\n"
    category = [
        "ملفات الادمن",
        "ملفات البوت",
        "ملفات المرح",
        "ملفات الميديا",
        "الادوات",
        "المرفقات",
        "الاضافيات",
    ]
    for cat in category:
        plugins = GRP_INFO[cat]
        outstr += f"**{hemojis[cat]} {cat.title()} ** - {len(plugins)}\n\n"
        for plugin in plugins:
            cmds = PLG_INFO[plugin]
            outstr += f"• **{plugin.title()} has {len(cmds)} commands**\n"
            for cmd in sorted(cmds):
                outstr += f"  - `{cmdprefix}{cmd}`\n"
            outstr += "\n"
    outstr += f"**👩‍💻 طريقة الاستخدام : ** `{cmdprefix}مساعدة <اسم الامر>`"
    return outstr


@catub.cat_cmd(
    pattern="^مساعدة ?(امر|-p|نص)? ?([\s\S]*)?",
    command=("مساعدة", plugin_category),
    info={
        "عمل الملف": "للحصول على دليل لــ NovemberBot .",
        "وصف الملف": "للحصول على معلومات أو تنفيذ الامر أو الملفات",
        "ملاحظة": "إذا كان اسم الأمر واسم الملف الإضافي متماثلين ، فستحصل على دليل للمكون الإضافي. لذلك باستخدام هذه العلامة تحصل على دليل الأوامر",
        "الاوامر": {
            "c": "للحصول على معلومات الاوامر",
            "p": "للحصول على معلومات من الملف المحدد",
            "t": "للحصول على جميع الملحقات في تنسيق نصي.",
        },
        "usage": [
            "مساعدة (اسم الملف/اسم الامر)",
            "مساعدة امر (اسم الامر)",
        ],
        "examples": ["مساعدة help", "مساعدة امر help"],
    },
)
async def _(event):
    "للحصول ع دليل شامل للملفات والاوامر"
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if flag and flag == "^امر" and input_str:  # -C
        outstr = await cmdinfo(input_str, event)
        if outstr is None:
            return
    elif input_str:
        outstr = await plugininfo(input_str, event, flag)
        if outstr is None:
            return
    elif flag == "^نص":
        outstr = await grpinfo()
    else:
        results = await event.client.inline_query(Config.TG_BOT_USERNAME, "^تعليمات")
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
        await event.delete()
        return
    await edit_or_reply(event, outstr)


@catub.cat_cmd(
    pattern="^استخدام(?:\s|$)([\s\S]*)",
    command=("استخدام", plugin_category),
    info={
        "اسم الملف": "لاظهار قائمة اوامر كل ملف",
        "وصف الملف": "if no input is given then will show list of all commands.",
        "طريقة الاستخدام": [
            "استخدام for all cmds",
            "{tr}cmds <plugin name> for paticular plugin",
        ],
    },
)
async def _(event):
    "لاظهار قائمة اوامر كل ملف."
    input_str = event.pattern_match.group(1)
    if not input_str:
        outstr = await cmdlist()
    else:
        try:
            cmds = PLG_INFO[input_str]
        except KeyError:
            return await edit_delete(event, "__Invalid plugin name recheck it.__")
        except Exception as e:
            return await edit_delete(event, f"**Error**\n`{e}`")
        outstr = f"• **{input_str.title()} has {len(cmds)} commands**\n"
        for cmd in cmds:
            outstr += f"  - `{cmdprefix}{cmd}`\n"
        outstr += f"**👩‍💻 Usage : ** `{cmdprefix}help -c <command name>`"
    await edit_or_reply(
        event, outstr, aslink=True, linktext="Total Commands of Catuserbot are :"
    )


@catub.cat_cmd(
    pattern="^امر ([\s\S]*)",
    command=("امر", plugin_category),
    info={
        "عمل الملف": "للبحث عن الاوامر",
        "مثل": "امر كتم",
    },
)
async def _(event):
    "للبحث عن الاوامر"
    cmd = event.pattern_match.group(1)
    found = [i for i in sorted(list(CMD_INFO)) if cmd in i]
    if found:
        out_str = "".join(f"`{i}`    " for i in found)
        out = f"**▾∮ لقد وجدت** `{len(found)}` **من الاوامر لـ ↫** `{cmd}`\n\n{out_str}"
        out += f"\n\n**▾↫ لمزيد من المعلومات تحقق** `مساعدة <الامر>`"
    else:
        out = f"**▾∮ لا يمكنني العثور على أي أمر **`{cmd}`** في نوفمبر**"
    await edit_or_reply(event, out)


@catub.cat_cmd(
    pattern="dc$",
    command=("dc", plugin_category),
    info={
        "header": "To show dc of your account.",
        "description": "Dc of your account and list of dc's will be showed",
        "usage": "{tr}dc",
    },
)
async def _(event):
    "To get dc of your bot"
    result = await event.client(functions.help.GetNearestDcRequest())
    result = f"**Dc details of your account:**\
              \n**Country :** {result.country}\
              \n**Current Dc :** {result.this_dc}\
              \n**Nearest Dc :** {result.nearest_dc}\
              \n\n**List Of Telegram Data Centres:**\
              \n**DC1 : **Miami FL, USA\
              \n**DC2 :** Amsterdam, NL\
              \n**DC3 :** Miami FL, USA\
              \n**DC4 :** Amsterdam, NL\
              \n**DC5 : **Singapore, SG\
                "
    await edit_or_reply(event, result)
