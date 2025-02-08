from app.core.llm.chat import get_chat
from worker import get_html

result = get_html.delay("https://stockapp.finance.qq.com/mstats/#mod=list&id=hs_hsj&module=hs&type=hsj")
cleaned_html =result.get(timeout=20)

chat = get_chat()
ss=chat.send_to_large_model("将页面中的新闻提取，提取字段为代码名称,最新价,涨跌幅,涨跌额,换手率,主力净流入,量比,振幅,成交量,成交额,将提取结果存为JSON数组",cleaned_html)
print(ss)