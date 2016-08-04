"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import mock
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from .views import index
from payments.models import User
from django.test import RequestFactory


class MainPageTests(TestCase):


    ###############
    #### Setup ####
    ###############

    @classmethod
    def setUpClass(cls):
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}

    #########################
    #### Testing Routes ####
    #########################

    # Verifies that '/' resolves to main.views.index function
    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    # Verifies that index view returns HTML
    def test_returns_appropriate_html_code(self):
        resp = index(self.request)
        self.assertEquals(resp.status_code, 200)

    #####################################
    #### Testing Templates and Views ####
    #####################################

    # Verifies returned template content against expected content
    def test_returns_exact_html(self):
        resp = index(self.request)
        self.assertEquals(
            resp.content,
            render_to_response("index.html").content
        )

    # Verifies that the correct template is returned for logged in users
    def test_index_handles_logged_in_user(self):
        # Create a session that appears to have a logged-in user
        self.request.session = {"user": "1"}

        with mock.patch('main.views.User') as user_mock:

            # Tell the mock what to do when called
            config = {'get_by_id.return_value': mock.Mock()}
            user_mock.configure_mock(**config)

            # request the index page
            resp = index(self.request)

            # ensures we return the state of the session back to normal so
            # we don't affect other tests
            self.request.session = {}

            # verifies it returns the page for the logged in user
            expectedHtml = render_to_response('user.html', {'user': user_mock.get_by_id(1)})
            self.assertEquals(resp.content, expectedHtml.content)
