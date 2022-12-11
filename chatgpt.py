from revChatGPT.revChatGPT import Chatbot
from nonebot import CommandSession, on_command, on_natural_language, NLPSession
from nonebot import permission as perm

config = {
    "Authorization": "<Your Bearer Token Here> Optional.",
    "session_token": "Put Your Session Token Here:)"}
gpt = Chatbot(config)

conversation_id = None
parent_id = None
qq = None

@on_command("!startchatgpt", permission=perm.SUPERUSER, only_to_me=True)
async def startchatgpt(session: CommandSession):
    global qq
    if qq:
        await session.finish("当前有人正在使用chatgpt!请稍后再试!")
    else:
        qq = str(session.ctx['user_id'])
        gpt.reset_chat()
        await session.send("成功开启chatgpt!")

@on_command("!stopchatgpt", only_to_me=True, permission=perm.SUPERUSER)
async def stopchatgpt(session: CommandSession):
    global qq, parent_id, conversation_id
    qq = None
    parent_id = None
    conversation_id = None
    await session.send("成功关闭chatgpt!")

@on_command("!reset", only_to_me=True, permission=perm.SUPERUSER)
async def reset(session: CommandSession):
    global qq
    if qq == str(session.ctx['user_id']):
        gpt.reset_chat()
        await session.send("对话已重置!")

@on_natural_language(only_to_me=True, only_short_message=False, permission=perm.SUPERUSER)
async def chatgpt(session: NLPSession):
    global qq, conversation_id, parent_id
    try:
        if str(session.ctx['user_id']) == qq:
            if parent_id and conversation_id:
                gpt.conversation_id = conversation_id
                gpt.parent_id = parent_id
            msg = session.msg_text.strip()
            res = gpt.get_chat_response(msg)
            conversation_id = res["conversation_id"]
            parent_id = res["parent_id"]
            await session.send(res['message'])
    except Exception as e:
        await session.send(str(e))
