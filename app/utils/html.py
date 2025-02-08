from bs4 import BeautifulSoup

def extract_text_and_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # 移除不需要的标签（如script、style、img等）
    for tag in soup(['script', 'style', 'img', 'link', 'meta', 'noscript']):
        tag.decompose()
    
    # 提取文本和标签
    extracted_content = soup.get_text(separator=' ', strip=True)
    
    # 如果需要保留标签结构，可以返回处理后的HTML
    cleaned_html = str(soup)
    
    return cleaned_html, extracted_content