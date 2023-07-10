import os
from dotenv import load_dotenv

load_dotenv(".env")

bind = os.getenv("WEB_HOST") + ":" + str(os.getenv("WEB_PORT"))
accesslog = "-"
access_log_format = '%(t)s %({x-forwarded-for}i)s %(l)s "%(r)s" %(s)s'  # "%(a)s"'
