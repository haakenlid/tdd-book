""" Test lists for logged in user. """

# from selenium.webdriver.common.keys import Keys
# from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
# from django.contrib.sessions.backends.db import SessionStore
# User = get_user_model()

from .base import FunctionalTest

TEST_EMAIL = 'edith@example.com'


class MyListsTest(FunctionalTest):

    test_browser = 'Firefox'  # PhantomJS(faster) or Chrome or Firefox

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edit is a logged-in user

        self.create_pre_authenticated_session(TEST_EMAIL)

        # She goes to the home page and starts a list
        list_items = [
            'Reticulate splines',
            'Immanentize eschaton',
        ]
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(list_items[0] + '\n')
        self.get_item_input_box().send_keys(list_items[1] + '\n')
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time.
        self.browser.find_element_by_link_text('My lists').click()

        # She sses that her list is in there, named according to its
        # first list item.
        self.browser.find_element_by_link_text(list_items[0]).click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decides to start another list, just to see.
        list_items.append('Click cows')
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(list_items[-1] + '\n')
        second_list_url = self.browser.current_url

        # Under "my lists" , her new list appears.
        self.browser.find_element_by_link_text('My lists').click()
        self.browser.find_element_by_link_text(list_items[-1]).click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The "My lists" option disappears.
        self.browser.find_element_by_id('id_logout').click()
        self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        )
