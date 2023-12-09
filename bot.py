from typing import Final
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pytube import YouTube

TOKEN : Final = 'your_api_token_here'
BOT_USERNAME: Final = '@your-bot_username_here'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Welcome to my bot! Please send the link of the desired YouTube video to get started")


#Responses

def handle_response(link):
    

    yt = YouTube(link)
    audio = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
    print(audio)
    stream = audio.download()
    return stream
    

# Logs incase if errors
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    link = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{link}"')

    

    response = handle_response(link)
    print("Bot: ", response)
    audio_file = InputFile(response)
    await context.bot.send_audio(chat_id=update.message.chat_id, audio=audio_file)
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    #Polling (Checks for new messages from users)
    print('Polling...')
    app.run_polling(poll_interval=3)
