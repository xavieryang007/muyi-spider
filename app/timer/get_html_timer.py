import re
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import timedelta
import logging

from app.core.browser.browser import get_page_html_with_out_disable_tags, get_page_html_with_out_disable_tags_async
from app.core.llm.chat import get_chat
from app.model.webui_params import Params


import asyncio

from app.utils.email import EmailUtils
from worker import get_html
# 初始化调度器
scheduler = BackgroundScheduler()
scheduler.start()

def init_timer(schedule_type, interval=None, daily_time=None,params:Params=None):
    """初始化定时任务
    Args:
        schedule_type (str): 调度类型，'间隔时间' 或 '指定时间'
        interval (dict): 当schedule_type为'间隔时间'时，包含小时、分钟、秒数的字典
        daily_time (datetime.time): 当schedule_type为'指定时间'时，每日执行时间
    """
    try:
        # 先移除所有现有任务
        scheduler.remove_all_jobs()
        
        if schedule_type == "间隔时间":
            # 计算总秒数
            total_seconds = (interval.get('hours', 0) * 3600 +
                           interval.get('minutes', 0) * 60 +
                           interval.get('seconds', 0))
            
            # 创建间隔触发器
            trigger = IntervalTrigger(seconds=total_seconds)
        else:
            # 创建每日定时触发器
            trigger = CronTrigger(hour=daily_time.hour,
                                minute=daily_time.minute,
                                second=daily_time.second)
        
        # 添加任务
        scheduler.add_job(
            execute_task,
            kwargs=params,
            trigger=trigger,
            id='html_crawler_task'
        )
        
        logging.info(f"定时任务已启动，调度类型: {schedule_type}")
    except Exception as e:
        logging.error(f"定时任务初始化失败: {str(e)}")
        raise

def stop_timer():
    """停止定时任务"""
    try:
        scheduler.remove_all_jobs()
        logging.info("定时任务已停止")
    except Exception as e:
        logging.error(f"定时任务停止失败: {str(e)}")
        raise

def execute_task(**options):
    """执行定时任务"""
    #asyncio.run(worker(options))
    result = get_html.delay(options['url'])
    cleaned_html =result.get(timeout=20)
    chat = get_chat()
    results =  chat.send_to_large_model(options['extract_prompt'],cleaned_html)
    results = re.sub(r'<think>.*?</think>', '', results, flags=re.DOTALL)
    checkResult = chat.check_by_large_model("你是数据检测专家，根据下面检测目标，如果数据符合检测目标要求，则进行<符合要求>，否则返回<数据缺失>",options['verify_prompt'],results)
    checkResult = re.sub(r'<think>.*?</think>', '', checkResult, flags=re.DOTALL)
    if "符合要求" not in checkResult:
        print("检测结果不符合要求")
        return
    
    print("检测结果符合要求")
    """
        发送邮件
        
        :param to_emails: 收件人邮箱列表
        :param subject: 邮件主题
        :param content: 纯文本内容
        :param html_content: HTML内容，默认为None
        """
    EmailUtils.send_email(to_emails=options['email'],
                          subject="通知邮件",
                          content=results,
                         SMTP_USERNAME= options['smtp_user'],
                         SMTP_PASSWORD= options['smtp_password'],
                         SMTP_SERVER= options['smtp_server'],
                         SMTP_PORT= options['smtp_port']
                         )
