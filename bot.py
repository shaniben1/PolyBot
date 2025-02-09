from telegram.ext import Updater, MessageHandler, Filters
from utils import search_download_youtube_video
from loguru import logger
import os.path


class Bot:

    download_path_video = []

    def __init__(self, token):
        # create frontend object to the bot programmer
        self.updater = Updater(token, use_context=True)

        # add _message_handler as main internal msg handler
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self._message_handler))

    def start(self):
        """Start polling msgs from users, this function never returns"""
        self.updater.start_polling()
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....')
        self.updater.idle()


    def _message_handler(self, update, context):
            """Main messages handler"""
            self.send_text(update, f'Your original message: {update.message.text}')




    def send_text(self, update,  text, quote=False):
        """Sends text to a chat"""
        # retry https://github.com/python-telegram-bot/python-telegram-bot/issues/1124
        update.message.reply_text(text, quote=quote)

    def send_video(self, update, context, file_path):
        """Sends video to a chat"""
        context.bot.send_video(chat_id=update.message.chat_id, video=open(file_path, 'rb'), supports_streaming=True)

class QuoteBot(Bot):
    def _message_handler(self, update, context):
        to_quote = True

        if update.message.text == 'Don\'t quote me please':
            to_quote = False

        self.send_text(update, f'Your original message: {update.message.text}', quote=to_quote)


class YoutubeBot(Bot):

    def _message_handler(self, update, context):

        for search_song in Bot.download_path_video:
            basename=os.path.basename(search_song)
            if basename==self.update.message.text:
                 return self.send_video(update, self.update.message.text, search_song)

        download_path_video = search_download_youtube_video(update.message.text)
        return self.send_video(update, self.update.message.text, download_path_video)


if __name__ == '__main__':
    with open('.telegramToken') as f:
        _token = f.read()


    my_bot = Bot(_token.strip())
    my_bot.start()

