from EdgeGPT import Chatbot
from nonebot import CommandSession, on_command, on_natural_language, NLPSession
from nonebot import permission as perm

gpt = None
qq = None

@on_command("!startchatbot", permission=perm.SUPERUSER, only_to_me=True)
async def startchatgpt(session: CommandSession):
    global qq, gpt
    if qq:
        await session.finish("当前有人正在使用chatbot!请稍后再试!")
    else:
        qq = str(session.ctx['user_id'])
        gpt = Chatbot(cookiePath="cookie.json")
        await session.finish("成功开启chatbot!")

@on_command("!stopchatbot", only_to_me=True, permission=perm.SUPERUSER)
async def stopchatbot(session: CommandSession):
    global qq, gpt
    if qq:
        qq = None
        await gpt.close()
        gpt = None
        await session.finish("成功关闭chatbot!")
    await session.finish("Chatbot尚未开启!")

@on_command("!reset", only_to_me=True, permission=perm.SUPERUSER)
async def reset(session: CommandSession):
    global qq
    if qq == str(session.ctx['user_id']):
        await gpt.reset()
        await session.send("对话已重置!")

@on_natural_language(only_to_me=True, only_short_message=False, permission=perm.SUPERUSER)
async def chatbot(session: NLPSession):
    global qq, gpt
    try:
        if str(session.ctx['user_id']) == qq:
            msg = session.msg_text.strip()
            res = await gpt.ask(msg)
            msg = ""
            for i in res['item']['messages']:
                if i["author"] == "bot":
                    msg = msg + i["text"]
            await session.send(msg)
    except Exception as e:
        await session.send(str(e))