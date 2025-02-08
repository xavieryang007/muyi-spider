from app.core.browser.browser import get_page_html_with_out_disable_tags
from app.core.llm.chat import get_chat


def ScawlerServiceRequest(BaseModel):
    url:str 
    goal:str 
    check:str 
def scawler_service(scawlerRequest:ScawlerServiceRequest):
    cleaned_html, extracted_text = get_page_html_with_out_disable_tags(scawlerRequest.url)
    chat = get_chat()
    content = chat.send_to_large_model(scawlerRequest.goal,cleaned_html)
    content.content