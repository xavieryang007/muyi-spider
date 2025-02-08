from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Optional, List
from pydantic import EmailStr


class EmailUtils:
    @staticmethod
    async def send_email(
        to_emails: Optional[EmailStr],
        subject: str,
        content: str,
        html_content: Optional[str] = None,
        SMTP_USERNAME: Optional[str] = None,
        SMTP_PASSWORD: Optional[str] = None,
        SMTP_SERVER: Optional[str] = None,
        SMTP_PORT: Optional[int] = None,
    ):
        """
        发送邮件
        
        :param to_emails: 收件人邮箱列表
        :param subject: 邮件主题
        :param content: 纯文本内容
        :param cc_emails: 抄送邮箱列表，默认为None
        :param bcc_emails: 密送邮箱列表，默认为None
        :param html_content: HTML内容，默认为None
        """
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_emails
        # 添加纯文本部分
        text_part = MIMEText(content, "plain", "utf-8")
        msg.attach(text_part)

        # 添加HTML部分（如果存在）
        if html_content:
            html_part = MIMEText(html_content, "html", "utf-8")
            msg.attach(html_part)

        # 连接SMTP服务器并发送邮件
        try:
            with smtplib.SMTP(
                SMTP_SERVER, SMTP_PORT, timeout=10
            ) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                all_recipients = to_emails.copy()
                server.sendmail(
                    SMTP_USERNAME, all_recipients, msg.as_string()
                )
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}")
