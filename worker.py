from celery import Celery

from app.core.browser.browser import get_page_html_with_out_disable_tags
from app.core.config.config import get_config
import tempfile

sysConfig = get_config()
# #'redis://localhost:6379/0'
app = Celery('tasks', broker=sysConfig.redis,backend=sysConfig.redis)


@app.task
def get_html(url: str):
    try:
        cleaned_html, extracted_text = get_page_html_with_out_disable_tags(url)
        return cleaned_html
    except Exception as e:
        print(e)
    return ""
