for _ in range(2):
    try:
        import vk_api, requests, re, io
        from aiogram import Bot, Dispatcher, executor, types
        from aiogram.dispatcher import filters
    except:
        import os, sys
        os.system(sys.executable + ' -m pip install aiogram vk_api')

from tgbottokens import *

#longpoll = VkBotLongPoll(vk, 214578909)
CHATID = 2
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
admin = 493595535

vk = vk_api.VkApi(token=vktoken)
try:
    vk_me = vk_api.VkApi(token=video_token)

except vk_api.exceptions.ApiError:
    tokenlink = "https://oauth.vk.com/oauth/authorize?client_id=51624586&display=page&redirect_uri=vk.com&scope=videos&response_type=token&v=5.131"
    bot.send_message(admin, f'Токен просрочен, нужна повторная <a href="{tokenlink}">авторизация</a>, отправьте токен в ответ', parse_mode=types.ParseMode.HTML)


upload = vk_api.VkUpload(vk)
video_upload = vk_api.VkUpload(vk_me)


pic = re.compile(r'.*\.((jpg)|(png))')
def ispic(s):
    return pic.match(s) is not None

vid = re.compile(r'.*\.((mp4)|(webm))')
def isvid(s):
    return vid.match(s) is not None

def sendphoto(id, photo, text = '', ):
    global upload
    photo = upload.photo_messages(photo)
    attachment = f"photo{photo[0]['owner_id']}_{photo[0]['id']}_{photo[0]['access_key']}"
    return vk.method('messages.send', {'chat_id':id, 'message':text, 'attachment':attachment, 'random_id':0}, raw= True)
    


def video(id, video, text = ''):
    a = vk_me.method("video.save", {'is_private':' 1', 'privacy_view': 'all'})
    res = requests.post(a['upload_url'], files={'video_file': video}).json()
    attachment = f"video{res['owner_id']}_{res['video_id']}"
    return vk.method('messages.send', {'chat_id':id, 'message':text, 'attachment':attachment, 'random_id':0}, raw= True)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def sph(message: types.Message):
    photos = message.photo
    if len(photos):
        file_info = await bot.get_file(photos[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        text = message.caption
        sendphoto(CHATID, downloaded_file, text)

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def svd(message: types.Message):
    media = message.video
    file_info = await bot.get_file(media.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    text = message.caption
    video(CHATID, downloaded_file, text)
    #    await message.reply('Не получилось переслать: '+ str(e))


tex = re.compile(r'vk1\.a\.[\w]+')

@dp.message_handler(filters.Text(contains='vk1.a'))
async def changetoken(message: types.Message):
    if message.from_user != admin:
        stxt(message)
        return
    token = tex.findall(message.text)
    if len(token) == 0:
        message.reply('no token in msg')
    else:
        token = token[0]
        tkns = []
        with open ('tgbottokens.py', 'r') as f:
            tkns = list(f.readlines())
        j = re.compile('.*video_token.*')
        for i, e in enumerate(tkns):
            if j.match(e) is not None:
                tkns[i] = f'video_token = {token}'
        global video_token
        video_token = token
@dp.message_handler(content_types=types.ContentType.TEXT)
async def stxt(message: types.Message):
    text = message.text
    if message.entities is not None and len(message.entities) > 0:
        try:
            u = message.entities[-1].url
            print(u)
            if ispic(u):
                media = requests.get(u)
                sendphoto(CHATID, io.BytesIO(media._content), text)
                print('detected url photo')
                return
            if isvid(u):
                media = requests.get(u)
                video(CHATID, io.BytesIO(media._content), text)
                print('detected url video')
                return
        except Exception as e:
            print(e)
            pass
        return vk.method('messages.send', {'chat_id':CHATID, 'message':text, 'random_id':0, 'dont_parse_links':0})





@dp.message_handler(content_types=types.ContentType.ANY)
async def svd(message: types.Message):
    await message.reply("К сожалению я пока не умею это пересылать(")


"""
def upd():
    for event in longpoll.listen():
        if event.type == VkBotEventType.GROUP_JOIN:
            if event.from_chat:
                id = event.chat_id
                sendtxt(id, "айди этого чата: " + str(id))


async def scheduler():
    aioschedule.every().second.do(upd)
    while True:
        await aioschedule.run_pending()
        await sleep(1)


async def on_startup(x):
    create_task(scheduler())
"""
print('starting')
executor.start_polling(dp)