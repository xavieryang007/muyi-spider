from pydantic import BaseModel

from app.core.llm.chat import get_chat
#from app.task.html import get_html
from worker import get_html


class ScawlerRequest(BaseModel):
    url:str 
    goal:str 

def scawler(scawlerRequest:ScawlerRequest):
    result = get_html.delay(scawlerRequest.url)
    cleaned_html =result.get(timeout=20)
    chat = get_chat()
    return chat.send_to_large_model(scawlerRequest.goal,cleaned_html)