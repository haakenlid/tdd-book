""" Test that user can log in with Mozilla Persona """
# from unittest import skip
from .base import FunctionalTest

TEST_EMAIL = 'edith@mockmyid.com'

class LoginTest(FunctionalTest):

    test_browser = 'Firefox'

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Edith logs in with her email address.
        # Use mockmyid.com for test email.
        self.wait_for_element_with_id('authentication_email')
        self.browser.find_element_by_id(
            'authentication_email'
        ).send_keys(TEST_EMAIL)
        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Refreshing the page, she sees it's a real sessin login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Terrified of theis new feature, she reflexively clicks "logout".
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(TEST_EMAIL)

        # The "logged out" status also persists after a refresh.
        self.browser.refresh()
        self.wait_to_be_logged_out(TEST_EMAIL)