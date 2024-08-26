import requests
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re

TOKEN: Final = '7147905922:AAFPXxcBS3vdWmc0W0BrQ_EP2SsiyxhSzZY'
BOT_USERNAME: Final = '@Iesp0404_bot'

# Google Custom Search API credentials
GOOGLE_API_KEY: Final = 'AIzaSyDqzvNif6a5kJm_sc4EmJzSk5upzrvHE48'
GOOGLE_CX: Final = '92178ceca83294240'  # Custom Search Engine ID
ALLOWED_GROUP_ID: Final = -1001817635995  # Replace with your actual group ID

GIF_IMAGE_PATHS: Final = {
    'call': 'Image/call.gif',
    'go': 'Image/go.gif',
    'swing': 'Image/swing.gif',
    'hug': 'Image/hug.gif',
    'praise': 'Image/praise.gif',
    'scold': 'Image/scold.gif',
    'ignore': 'Image/ignore.gif',
    'chill': 'Image/chill.gif',
    'dance': 'Image/dance.gif',
    'move': 'Image/move.gif',
    'sorry': 'Image/sorry.gif',
    'fight': 'Image/fight.gif',
    'miss': 'Image/miss.gif',
    'write': 'Image/write.gif',
    'throw': 'Image/throw.gif',
    'kick': 'Image/kick.gif',
    'care': 'Image/care.gif',
    'snatch': 'Image/snatch.gif',
    'tease': 'Image/tease.gif',
    'stalk': 'Image/stalk.gif',
    'enjoy': 'Image/enjoy.gif',
    'play': 'Image/play.gif',
    'teach': 'Image/teach.gif',
    'slap': 'Image/slap.gif',
    'feed': 'Image/feed.gif',
    'poke': 'Image/poke.gif',
    'bite': 'Image/bite.gif',
    'greet': 'Image/greet.gif',
    'boom': 'Image/boom.gif',
    'beat': 'Image/beat.gif',
    'roast': 'Image/roast.gif',
    'fry': 'Image/fry.gif'
}

def clean_text(text: str) -> str:
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    return text
async def send_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text.split()[0][1:]
    file_path = GIF_IMAGE_PATHS.get(command)
    username = update.message.from_user.username
    target_user = re.search(r'@(\w+)', update.message.text)
    target_username = target_user.group(0) if target_user else 'someone'
    custom_message = f'@{username} is {command}ing {target_username}'

    if file_path:
        if file_path.endswith('.gif'):
            await update.message.reply_animation(animation=open(file_path, 'rb'), caption=custom_message)
        else:
            await update.message.reply_photo(photo=open(file_path, 'rb'), caption=custom_message)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks For Chatting With Me, I am YourBot.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('No worries, I will assist you with all kinds of help. For more help, contact @YourContactUsername.')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('For a custom command, I will respond in a customized way.')

# Function to get a response from Google Custom Search
async def get_google_search_response(query: str) -> str:
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query
    }
    try:
        response = requests.get(search_url, params=params)
        if response.status_code == 429:  # Check for quota exceeded
            return "I've reached my daily search limit. I'll be able to respond after tomorrow."
        response.raise_for_status()
        search_results = response.json()
        if 'items' in search_results:
            snippets = [clean_text(item.get('snippet', '')) for item in search_results['items']]
            return ' '.join(snippets)[:400]  # Limit response to 400 characters
        else:
            return 'No results found.'
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"Other error occurred: {err}"


# Command to handle Google Custom Search queries
# Command to handle Google Custom Search queries
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # Check if the command is being used in the allowed group
    if chat_id == ALLOWED_GROUP_ID:
        user_message = ' '.join(context.args)
        if user_message:
            response = await get_google_search_response(user_message)
            await update.message.reply_text(response)
        else:
            await update.message.reply_text('Please ask a question.')
    else:
        await update.message.reply_text('Sorry, this command is not allowed in this group. Join @iesp0404')

def handle_response(text: str) -> str:
    processed: str = text.lower()
    if re.search(r'\bhello\b|\bhi\b|\bhii\b|\bhii\b|\bhlo\b|\bhey\b', processed):
        return 'Hello, hi there! How are you?'
    if re.search(r'\bhow are you\b', processed):
        return 'I am just a bot, but I’m here to help you. How can I assist you?'
    if re.search(r'\bthank you\b|\bthanks\b|\bthank\b', processed):
        return 'You’re welcome! Let me know if you need anything else.'
    if re.search(r'\bbye\b|\bgoodbye\b', processed):
        return 'Goodbye! Have a great day!'
    if re.search(r'\bhelp\b', processed):
        return 'I am here to help! Just let me know what you need assistance with.'
    if re.search(r'\bsamaira\b', processed):
        return 'she is a nyc person'
    if re.search(r'\bpurpose of the group\b', processed):
        return 'To Improve English Speaking ✨Keep Learning Keep Growing✨'
    if re.search(r'\bwho is your owner\b', processed):
        return 'My Owner is Ishi'
    if re.search(r'\bgood morning\b\bgood mrng\b\bgm\b\bgood night\b\bgood nyt\b\bgn\b\bgd nyt\b\bgood afternoon\b\bgood noon\b', processed):
        return 'Jai Shree Krishna'
    if re.search(r'\bbook\b', processed):
        return '@shivanshUp'
    if re.search(r'\bquiz\b\bhead admin\b', processed):
        return '@shivanshUp'
    if re.search(r'\b management\b', processed):
        return '@cinderella_299 '
    if re.search(r'\boctopus\b\bcrocodile\b', processed):
        return '@Jimmyflu  @O000000000O00000000O'
    if re.search(r'\bchess\b', processed):
        return '@shivanshUp @Chiiiiikkuu @innocent_boy95 '
    if re.search(r'\brapid fire\b', processed):
        return '@maahi_raj001'

    return None

# Command to list all available commands
async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_list = '\n'.join([f'/{cmd}' for cmd in GIF_IMAGE_PATHS.keys()])
    all_commands = f"Available commands:\n{commands_list}\n/search"
    await update.message.reply_text(all_commands)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    print(f'User({update.message.chat.id}): "{text}"')
    if not text.startswith('/'):
        response = handle_response(text)
        if response:
            print('Bot:', response)
            await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    for command in GIF_IMAGE_PATHS.keys():
        app.add_handler(CommandHandler(command, send_media))

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('search', search_command))
    app.add_handler(CommandHandler('iespcommands', commands_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    print('Polling the bot...')
    app.run_polling(poll_interval=1)