from pydantic import BaseModel




class Params(BaseModel):
    """邮件/SMTP和Web UI的配置参数"""
    email:str = None  # 用于发送邮件的邮箱地址
    smtp_server:str = None  # SMTP服务器主机名
    smtp_port:int = None  # SMTP服务器端口号
    smtp_ssl:str = None  # 是否使用SSL连接SMTP (True/False)
    smtp_user:str = None  # SMTP认证用户名
    smtp_password:str = None  # SMTP认证密码
    extract_prompt:str = None  # 内容提取的提示模板
    verify_prompt:str = None  # 验证的提示模板
    url:str = None  # Web UI的基础URL
