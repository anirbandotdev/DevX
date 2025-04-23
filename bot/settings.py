from dotenv import load_dotenv
import os


load_dotenv()


TOKEN = os.environ["TOKEN"]
PREFIX = os.environ["PREFIX"]
COGS = ["Moderation" , "Music" , "Challenge"]
WAVELINK_URI = os.environ["WAVELINK_URI"]
WAVELINK_PASS = os.environ["WAVELINK_PASS"]
USER_FILE = "user.json"
CHALLENGE_FILE = "challenge.json"
ADMINS = [1288870270664179815,]
