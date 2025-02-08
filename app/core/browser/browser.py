from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

from app.utils.html import extract_text_and_tags
from playwright._impl._api_structures import (
    ViewportSize,
)
# 通过URL获取页面HTML
def get_page_html(url:str):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
				'--no-sandbox',
				'--disable-blink-features=AutomationControlled',
				'--disable-infobars',
				'--disable-background-timer-throttling',
				'--disable-popup-blocking',
				'--disable-backgrounding-occluded-windows',
				'--disable-renderer-backgrounding',
				'--disable-window-activation',
				'--disable-focus-on-load',
				'--no-first-run',
				'--no-default-browser-check',
				'--no-startup-window',
				'--window-position=0,0',
				# '--window-size=1280,1000',
                '--disable-web-security',
				'--disable-site-isolation-trials',
				'--disable-features=IsolateOrigins,site-per-process',
			]
            )
        page = browser.new_page(
            viewport = ViewportSize(
                width= 1280, height=1100
			),
			no_viewport=False,
			user_agent=	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
			java_script_enabled=True,
			bypass_csp=False,
			ignore_https_errors=False,
			record_video_dir=None,
			record_video_size=ViewportSize(
                width= 1280, height=1100
			),
			locale=None,
		)
        page.add_init_script(
            	"""
			// Webdriver property
			Object.defineProperty(navigator, 'webdriver', {
				get: () => undefined
			});

			// Languages
			Object.defineProperty(navigator, 'languages', {
				get: () => ['en-US']
			});

			// Plugins
			Object.defineProperty(navigator, 'plugins', {
				get: () => [1, 2, 3, 4, 5]
			});

			// Chrome runtime
			window.chrome = { runtime: {} };

			// Permissions
			const originalQuery = window.navigator.permissions.query;
			window.navigator.permissions.query = (parameters) => (
				parameters.name === 'notifications' ?
					Promise.resolve({ state: Notification.permission }) :
					originalQuery(parameters)
			);
			(function () {
				const originalAttachShadow = Element.prototype.attachShadow;
				Element.prototype.attachShadow = function attachShadow(options) {
					return originalAttachShadow.call(this, { ...options, mode: "open" });
				};
			})();
			"""
		)
        page.goto(url)
        html = page.content()
        browser.close()
    return html
# 通过URL获取去除指定标签后的HTML和文本
def get_page_html_with_out_disable_tags(url:str):
    htmlContent = get_page_html(url)
    # 提取标签和文本
    cleaned_html, extracted_text = extract_text_and_tags(htmlContent)
    return cleaned_html, extracted_text


        
# 通过URL获取页面HTML
async def get_page_html_async(url:str):
    async with async_playwright() as p:
        browser =await p.chromium.launch(
            headless=False,
            args=[
				'--no-sandbox',
				'--disable-blink-features=AutomationControlled',
				'--disable-infobars',
				'--disable-background-timer-throttling',
				'--disable-popup-blocking',
				'--disable-backgrounding-occluded-windows',
				'--disable-renderer-backgrounding',
				'--disable-window-activation',
				'--disable-focus-on-load',
				'--no-first-run',
				'--no-default-browser-check',
				'--no-startup-window',
				'--window-position=0,0',
				# '--window-size=1280,1000',
                '--disable-web-security',
				'--disable-site-isolation-trials',
				'--disable-features=IsolateOrigins,site-per-process',
			]
            )
        page = await browser.new_page(
            viewport = ViewportSize(
                width= 1280, height=1100
			),
			no_viewport=False,
			user_agent=	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
			java_script_enabled=True,
			bypass_csp=False,
			ignore_https_errors=False,
			record_video_dir=None,
			record_video_size=ViewportSize(
                width= 1280, height=1100
			),
			locale=None,
		)
        await page.add_init_script(
            	"""
			// Webdriver property
			Object.defineProperty(navigator, 'webdriver', {
				get: () => undefined
			});

			// Languages
			Object.defineProperty(navigator, 'languages', {
				get: () => ['en-US']
			});

			// Plugins
			Object.defineProperty(navigator, 'plugins', {
				get: () => [1, 2, 3, 4, 5]
			});

			// Chrome runtime
			window.chrome = { runtime: {} };

			// Permissions
			const originalQuery = window.navigator.permissions.query;
			window.navigator.permissions.query = (parameters) => (
				parameters.name === 'notifications' ?
					Promise.resolve({ state: Notification.permission }) :
					originalQuery(parameters)
			);
			(function () {
				const originalAttachShadow = Element.prototype.attachShadow;
				Element.prototype.attachShadow = function attachShadow(options) {
					return originalAttachShadow.call(this, { ...options, mode: "open" });
				};
			})();
			"""
		)
        await page.goto(url)
        html = await page.content()
        await browser.close()
    return html
# 通过URL获取去除指定标签后的HTML和文本
async def get_page_html_with_out_disable_tags_async(url:str):
    htmlContent = await get_page_html_async(url)
    # 提取标签和文本
    cleaned_html, extracted_text = extract_text_and_tags(htmlContent)
    return cleaned_html, extracted_text