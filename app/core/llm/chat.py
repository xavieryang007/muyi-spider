from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import SecretStr
from app.core.config.config import Config, get_config

class Chat():
    def __init__(self,config:Config):
        self.config = config
        self._initLLM()
    def _initLLM(self):
        if self.config.model_type and self.config.model_type.lower() == "ollama":
            self.llm = ChatOllama(model=self.config.model, num_ctx=32000)
        else:
            self.llm=ChatOpenAI(base_url=self.config.base_url, model=self.config.model, api_key=SecretStr(self.config.openai_api_key))
    def send_to_large_model(self,goal,content):
        # 假设你有一个大模型的API
        # 定义提示模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个网页内容提取专家，根据用户需要完成的目标和网页内容提出需要的数据，并返回JSON格式."),
            ("user", "{input}"),
        ])

        # 创建链式工作流
        chain = prompt | self.llm
        # 运行链式工作流
        response = chain.invoke({"input": "完成目标:"+goal+"\r\n网页详情:"+content})
        return response.content
    def check_by_large_model(self,system,goal,content):
        # 假设你有一个大模型的API
        # 定义提示模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("user", "{input}"),
        ])

        # 创建链式工作流
        chain = prompt | self.llm
        # 运行链式工作流
        response = chain.invoke({"input": "检测目标:"+goal+"\r\n数据详情:"+content})
        return response.model_dump_json()

sysConfig = get_config()
chat= Chat(sysConfig)

def get_chat():
    return chat