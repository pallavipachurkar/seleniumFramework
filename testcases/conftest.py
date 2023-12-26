import os

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# options.add_argument("--disable-notifications")
from selenium.webdriver.firefox.service import Service as FirefoxService

@pytest.fixture(scope="class")
def setup(request):
    # if browser == "chrome":
    #     driver = webdriver.Chrome()
    #     # driver = webdriver.Chrome(options=chrome_options)
    # elif browser == "firefox":
    #     # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    #     driver = webdriver.Firefox()
    # elif browser == "edge":
    #     # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    #     driver = webdriver.Edge()
    #
    # else:
    #     print("Provid valid browser")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.yatra.com/")
    driver.maximize_window()
    request.cls.driver = driver

    yield
    driver.close()

# def pytest_addoption(parser):
#     parser.addoption("--browser")
#
# @pytest.fixture(scope="class",autouse=True)
# def browser(request):
#     return request.config.getoption("--browser")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html=item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        # always add url to report
        extras.append(pytest_html.extras.url("https://www.yatra.com/"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            report_directory = os.path.dirname(item.config.option.htmlpath)
            file_name = report.nodeid.replace("::","_") + ".png"
            destinationfile = os.path.join(report_directory,file_name)
            driver.save_screenshot(destinationfile)
            if file_name:
                html='<div><img src="%s" alt="screenshot" style="width:300px; height:200px"'
                'onclick="window.open(this.src)" align="right" /></div>'%file_name
            extras.append(pytest_html.extras.html(html))
        report.extras = extras

def pytest_html_report_title(report):
    report.title = "RCV Academy Automation Report"