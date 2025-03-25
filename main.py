from src.dc import AuctionBot
from dotenv import load_dotenv
import os
from src.logger import setup_loggers
from src.db import create_db

setup_loggers()
load_dotenv()

def main():
    TOKEN = os.getenv('TOKEN')
    CHANNEL_ID  = int(os.getenv('CHANNEL_ID'))
    
    create_db()    
    auction_bot = AuctionBot(token=TOKEN,channel_id=CHANNEL_ID)
    auction_bot.run()

if __name__ == "__main__":
    main()