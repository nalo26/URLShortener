import os
from dotenv import load_dotenv

load_dotenv(".env")

bind = os.getenv("WEB_HOST") + ":" + str(os.getenv("WEB_PORT"))
