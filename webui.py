import streamlit as st
from datetime import time
import json
from datetime import time

from app.model.webui_params import Params

st.set_page_config(page_title="Web Crawler Configuration", layout="wide")

# 页面标题
st.title("智能网页数据抓取配置")
# 新增服务控制函数
def start_service(schedule_type, interval=None, daily_time=None,params:Params=None):
    """启动爬虫服务时的初始化操作"""
    try:
        print('start_service')
        # 初始化定时任务
        from app.timer.get_html_timer import init_timer
        init_timer(schedule_type, interval, daily_time,params)
        
        st.toast("✅ 服务已启动", icon="🚀")
    except Exception as e:
        st.error(f"服务启动失败: {str(e)}")
        st.session_state.service_running = False

def stop_service():
    """停止服务时的清理操作"""
    try:
        print('stop_service')
        # 停止定时任务
        from app.timer.get_html_timer import stop_timer
        stop_timer()
        
        st.toast("⛔ 服务已停止", icon="🛑")
    except Exception as e:
        st.error(f"服务停止失败: {str(e)}")
        st.session_state.service_running = True

with st.form("crawler_config"):
    # 网址输入
    url = st.text_input("目标网址", placeholder="请输入要抓取的完整网址（包含http/https）")
    
    # 双栏布局
    col1, col2 = st.columns(2)
    
    with col1:
        # 数据抓取提示词
        extract_prompt = st.text_area("数据提取提示词", 
                                    height=150,
                                    placeholder="请描述需要提取的数据特征，例如：\n- 提取所有产品名称和价格\n- 提取新闻标题和发布时间\n- 表格中的第三列数据")
    
    with col2:
        # 验证提示词
        verify_prompt = st.text_area("数据验证提示词",
                                   height=150,
                                   placeholder="请输入验证数据准确性的条件，例如：\n- 价格应为数字且大于0\n- 发布时间格式应为YYYY-MM-DD\n- 标题长度不超过100字符")

    # 接收邮箱和SMTP配置
    st.subheader("基本配置项")
    email = st.text_input("通知邮箱 *", placeholder="请输入接收通知的email地址", help="必填项")
    
    with st.expander("高级SMTP配置(可选)", expanded=False):
        st.caption("用于发送通知邮件的SMTP服务器设置")
        cols_smtp = st.columns(3)
        with cols_smtp[0]:
            smtp_server = st.text_input("SMTP服务器地址", placeholder="smtp.example.com")
        with cols_smtp[1]:
            smtp_port = st.number_input("端口号", value=465, min_value=1, max_value=65535)
        with cols_smtp[2]:
            smtp_ssl = st.selectbox("加密方式", options=["SSL", "STARTTLS"], index=0)
            
        smtp_user = st.text_input("账号（邮箱）", placeholder="yourname@example.com")
        smtp_password = st.text_input("密码", type="password")
    
    # 调度时间设置
    st.subheader("抓取计划设置")
    schedule_type = st.radio("调度类型", 
                           options=["间隔时间", "指定时间"],
                           horizontal=True)

    if schedule_type == "间隔时间":
        interval_cols = st.columns(3)
        with interval_cols[0]:
            hours = st.number_input("小时", min_value=0, max_value=23, value=0)
        with interval_cols[1]:
            minutes = st.number_input("分钟", min_value=0, max_value=59, value=5)
        with interval_cols[2]:
            seconds = st.number_input("秒数", min_value=0, max_value=59, value=0)
    else:
        daily_time = st.time_input("每日执行时间", value=time(9, 0))

    # 初始化状态（移到表单外部）
    if 'service_running' not in st.session_state:
        st.session_state.update({
            'service_running': False,
            'last_operation': None
        })
    
    # 动态按钮配置
    if st.session_state.service_running:
        btn_label = "🛑 停止服务"
        btn_type = "secondary"
    else:
        btn_label = "🚀 启动服务"
        btn_type = "primary"

    # 服务控制按钮（单按钮切换状态）
    submitted = st.form_submit_button(btn_label, type=btn_type)

    if submitted:
        import re
        # 基础验证
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        errors = []
        if not email.strip():
            errors.append("必须填写通知邮箱")
        elif not re.match(email_pattern, email):
            errors.append("邮箱格式不正确")
        if not url.strip():
            errors.append("必须填写目标网址")
        elif not url.startswith(("http://", "https://")):
            errors.append("网址必须包含http://或https://协议头")

        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                # 获取当前状态并执行操作
                target_state = not st.session_state.service_running
                print('target_state')
                print(target_state)
                # 执行服务操作
                if target_state:

                    _params = Params(
                        email = email,
                        smtp_server = smtp_server,
                        smtp_port = smtp_port,
                        smtp_ssl = smtp_ssl,
                        smtp_user = smtp_user,
                        smtp_password = smtp_password,
                        extract_prompt = extract_prompt,
                        verify_prompt = verify_prompt,
                        url = url,
                    )
                    # 根据调度类型传递参数
                    if schedule_type == "间隔时间":
                        interval = {
                            'hours': hours,
                            'minutes': minutes, 
                            'seconds': seconds
                        }
                        start_service(schedule_type, interval=interval,params= _params)
                    else:
                        start_service(schedule_type, daily_time=daily_time,params= _params)
                else:
                    stop_service()
                
                # 仅在操作成功后更新状态
                st.session_state.service_running = target_state
                
                # 状态更新后立即执行界面刷新
                st.session_state.last_operation = 'service_toggle'
                st.rerun()
                
            except Exception as e:
                print(e)
                st.error(f"服务操作失败: {str(e)}")
                # 状态回滚并强制刷新
                st.session_state.service_running = not target_state
                st.session_state.last_operation = 'rollback'
                st.rerun()
