import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_insider_qa_jobs_page_opens():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor=os.environ["SELENIUM_REMOTE_URL"],
        options=options
    )

    driver.get("https://useinsider.com/careers/quality-assurance/")
    time.sleep(5)

    see_all_jobs = driver.find_element(By.LINK_TEXT, "See all QA jobs")
    assert see_all_jobs.is_displayed()

    driver.quit()
