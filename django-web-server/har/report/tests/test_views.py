from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from har.report.views import render_connection_view


class TestConnectionPage(TestCase):


    def test_root_url_resolves_to_connection_page_view(self):
        # to resolve URLs and find what view function they should map to
        found = resolve('/')
        self.assertEqual(found.func, render_connection_view)

    def test_connection_page_return_correct_html(self):

        response = self.client.get("/")
        html = response.content.decode('utf-8')
        self.assertEquals(response.status_code, 200)
        self.assertIn('<title>Connection</title>', html)
        self.assertTemplateUsed(response, 'connection.html')
