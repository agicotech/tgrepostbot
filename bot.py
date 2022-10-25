import vk_api, requests
from aiogram import Bot, Dispatcher, executor, types
from token import *
vk = vk_api.VkApi(token=vktoken)
#longpoll = VkBotLongPoll(vk, 214578909)
CHATID = 2

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
lastid = None

def sendphoto(id, photo, text = '', ):
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(photo)
    attachment = f"photo{photo[0]['owner_id']}_{photo[0]['id']}_{photo[0]['access_key']}"
    vk.method('messages.send', {'chat_id':id, 'message':text, 'attachment':attachment, 'random_id':0})

def sendvideo(id, video, text = ''):
    upload = vk_api.VkUpload(vk)
    video = upload.video(video)
    attachment = f"video{video[0]['owner_id']}_{video[0]['id']}_{video[0]['access_key']}"
    vk.method('messages.send', {'chat_id':id, 'message':text, 'attachment':attachment, 'random_id':0})

def video(id, video, txt):
    a = vk.method("video.save")
    b = requests.post(a['upload_url'], files={'video': video}).json()
    #c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    vk.method("messages.send", {"peer_id": id, "message": txt, "attachment": f'video{b["owner_id"]}_{b["video_id"]}'})


async def tgmention(username: str):
    link = vk.method("utils.getShortLink", {"url":("https://t.me/"+ username)})['short_url']
    ment = '[{}|{}]'.format(link, '@'+username)
    return ment

def sendtxt(id, text):
    vk.method('messages.send', {'chat_id':id, 'message':text, 'random_id':0})

@dp.message_handler(commands='start')
async def cmd(message: types.Message):
    await message.answer('Привет! Пересылай мне мемы и они попадут в беседу. Я умею работать с картинками и текстом')

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def sph(message: types.Message):
    global lastid
    photos = message.photo
    if len(photos):
        file_info = await bot.get_file(photos[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        text = message.caption
        if lastid != message.from_user.id:
            ds = ('\nby @{}'.format(message.from_user.username))
            if text == None:
                text = ds
            else: text += ds 
            lastid = message.from_user.id
        sendphoto(CHATID, downloaded_file, text)

@dp.message_handler(content_types=types.ContentType.TEXT)
async def stxt(message: types.Message):
    global lastid
    text = message.text
    if lastid != message.from_user.id:
        text += '\nby @{}'.format(message.from_user.full_name)
        lastid = message.from_user.id
    #if type(message.from_user.username) == str:
    #        text += '\nhttps://t.me/' + message.from_user.username
    sendtxt(CHATID, text)

@dp.message_handler(content_types=types.ContentType.ANY)
async def svd(message: types.Message):
    await message.reply("К сожалению я пока не умею это пересылать(")


print('starting')
executor.start_polling(dp)