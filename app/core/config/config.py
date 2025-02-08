import os 
from pydantic import BaseModel
from typing import Awaitable, Callable, Optional, Tuple
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()
class Config(BaseModel):
    """
    配置模型类，用于定义应用程序所需的配置参数。
    """
    model_type: Optional[str] = None
    """模型类型"""
    openai_api_key: Optional[str] = None
    """OpenAI API密钥"""
    base_url: Optional[str] = None
    """基础URL地址"""
    model: Optional[str] = None
    """使用的模型名称"""
    redis:Optional[str] = None 
    """redis配置信息"""

def get_config():
    model_type = os.getenv("MODEL_TYPE")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("BASE_URL")
    model = os.getenv("MODEL")
    redis = os.getenv("REDIS")
    # 创建Config实例并验证数据
    config = Config(
        model_type=model_type,
        openai_api_key=openai_api_key,
        base_url=base_url,
        model=model,
        redis=redis
    )
    return config