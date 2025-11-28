from django.test import TestCase


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        # rather than targeting specific html, we can target correct template used
        self.assertTemplateUsed(response, "home.html")

    def test_homepage_content(self):
        response = self.client.get("/")
        # smoke test: check system is doing one very simple thing correctly
        self.assertContains(response, "To-Do")
