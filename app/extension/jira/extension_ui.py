import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, AdminPage
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
    #         login_page.wait_for_login_page_loaded()
    #         login_page.set_credentials(username=username, password=password)
    #         login_page.wait_for_dashboard_or_first_login_loaded()
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #         # uncomment below line to do web_sudo and authorise access to admin pages
    #         # AdminPage(webdriver).go_to(password=password)
    #
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

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
        # IMPORTANT
        # This action will attach issues to the second project in the dropdown list.
        # Ensure that the Zeplin user has access to test or dummy projects to avoid affecting real data.
        # Remove all these attachments from the issue after the tests are completed.
        xpath_to_project = '//*[@id="dropdown-projects"]/div/div[2]'
        page.wait_until_visible((By.XPATH, xpath_to_project))
        page.get_element((By.XPATH, xpath_to_project)).click()
        page.wait_until_invisible((By.ID, "resources"))

    measure()
