"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from .views import index
from payments.models import User
from django.test import RequestFactory


class MainPageTests(TestCase):

    # Verifies that '/' resolves to main.views.index function
    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    # Verifies that index view returns HTML
    def test_returns_appropriate_html(self):
        index = self.client.get('/')
        self.assertEquals(index.status_code, 200)

    # Verifies that the correct template is returned
    def test_uses_index_html_template(self):
        index = self.client.get('/')
        self.assertTemplateUsed(index, "index.html")

    # Verifies returned template content against expected content
    def test_returns_exact_html(self):
        index = self.client.get('/')
        self.assertEquals(
            index.content,
            render_to_response("index.html").content
        )

    # Verifies that the correct template is returned for logged in users
    def test_index_handles_logged_in_user(self):
        # creates the user needed for user lookup from index page
        user = User(
            name='jj',
            email='j@j.com',
        )
        user.save()

        # creates a mock request object
        request_factory = RequestFactory()
        request = request_factory.get('/')

        # creates a session that appears to have a logged in user
        request.session = {"user": "1"}

        # requests the index page
        resp = index(request)

        # verifies it returns the page for the logged in user
        self.assertTemplateUsed(
            resp.content,
            render_to_response('user.html', {'user': user}).content
        )
