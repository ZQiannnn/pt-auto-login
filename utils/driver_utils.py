import logging
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class DriverUtils:

    @classmethod
    def get_driver(cls):
        try:
            logging.info("启动 Selenium")

            global chrome_options
            chrome_options = webdriver.ChromeOptions()

            # 青龙面板特定的 Chrome 选项
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument('--headless=new')  # 使用新的 headless 模式
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument("--disable-popup-blocking")

            # 添加 user-agent
            chrome_options.add_argument(
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

            # 禁用自动化标志
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # 设置页面加载策略
            chrome_options.page_load_strategy = 'normal'

            # 检查 chromedriver 路径
            global chromedriver_path
            chromedriver_path = shutil.which("chromedriver")

            if not chromedriver_path:
                logging.error("chromedriver 未找到，请确保已安装并配置正确的路径。")
                exit(1)
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # 删除 navigator.webdriver 标志
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })

            # 设置页面加载超时
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)

            return driver

        except Exception as e:
            logging.error(f"创建 WebDriver 失败: {e}")

    @classmethod
    def close_driver(cls, driver):
        driver.quit()
