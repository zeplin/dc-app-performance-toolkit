import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS

ISSUES = "issues"

def view_zeplin_section(webdriver, datasets):
    page = BasePage(webdriver)

    issue = random.choice(datasets[ISSUES])
    issue_key = issue[0]

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.set_credentials(username=username, password=password)
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')

    @print_timing("selenium_zeplin_for_jira_zeplin_section")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
        page.wait_until_visible((By.ID, "zeplin-panel"))
        page.wait_until_visible((By.ID, "attached-resources"))

    measure()


def use_zeplin_attachment_dropdown(webdriver, datasets):
    page = BasePage(webdriver)

    issue = random.choice(datasets[ISSUES])
    issue_key = issue[0]

    @print_timing("selenium_zeplin_for_jira_attachments_dropdown")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
        page.wait_until_visible((By.ID, "zeplin-panel"))
        page.wait_until_visible((By.ID, "attached-resources"))
        page.wait_until_clickable((By.ID, "attach-button"))
        page.get_element((By.ID, "attach-button")).click()
        page.wait_until_visible((By.ID, "resources"))
        page.wait_until_clickable((By.ID, "screens-link"))
        page.get_element((By.ID, "projects-link")).click()
        page.wait_until_visible((By.XPATH, '//*[@id="dropdown-projects"]/div/div[2]'))
        page.get_element((By.XPATH, '//*[@id="dropdown-projects"]/div/div[2]')).click()
        page.wait_until_invisible((By.ID, "resources"))

    measure()