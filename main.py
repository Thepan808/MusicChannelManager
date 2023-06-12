from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
import json
import logging
import mutagen
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


token = os.environ.get('BOT_TOKEN')
updater = Updater(token)
dispatcher = updater.dispatcher

class Audio:
    def __init__(self, bot, update):
        self.bot = bot
        self.update = update
        self.chat_id = update.effective_message.chat_id
        self.message_id = update.effective_message.message_id
        self.audio = self.download_audio()

    def download_audio(self):
        audio = self.update.effective_message.effective_attachment
        file_id = audio.file_id
        new_file = self.bot.get_file(file_id)

        logging.log(logging.INFO, "Downloading file")
        self.bot.edit_message_caption(chat_id=self.chat_id, message_id=self.message_id, caption="Legendando...")

        new_file.download('file.mp3')
        logging.log(logging.INFO, "File downloaded")

        return mutagen.File('file.mp3')

    def set_new_caption(self):
        title = ""
        artist = ""
        album = ""
        genre = ""
        try:
            title = self.audio.tags["TIT2"]
        except:
            pass
        try:
            artist = self.audio.tags["TPE1"]
        except:
            pass
        try:
            album = self.audio.tags["TALB"]
        except:
            pass
        try:
            genre = self.audio.tags["TCON"]
        except:
            pass

        new_caption = '''✏️ Título: {0}
👤 Artista: {1}
💽 Álbum:  {2}
🎼 Gênero: {3}'''.format(title, artist, album, genre)

        self.bot.edit_message_caption(chat_id=self.chat_id, message_id=self.message_id, caption=new_caption)
        logging.log(logging.INFO, "Caption changed")


def change_caption(bot, update):
    logging.log(logging.INFO, "Changing caption")
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id

    audio = Audio(bot, update)
    audio.set_new_caption()


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='Hi !  I am Music Channel Manager Bot!\nI can add a dynamic caption to the musics, just add me to a channel as admin and give me the permissions.')


handler = MessageHandler(Filters.audio, change_caption, channel_post_updates=True, message_updates=False)
handlers = CommandHandler('zzz', start)
dispatcher.add_handler(handler=handler)
dispatcher.add_handler(handler=handlers)


POLLING_INTERVAL = 0.2
updater.start_polling(poll_interval=POLLING_INTERVAL)
updater.idle()
