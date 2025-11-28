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

    def test_renders_input_form(self):
        response = self.client.get("/")
        self.assertContains(response, '<form method="POST">')
        # assertContains does simple substring formatting, so it will
        #  include newlines, spaces, tabs etc. So we are just going to use
        #  two assertions for now
        self.assertContains(response, '<input')
        self.assertContains(response, 'name="item_text"')

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertContains(response, "A new list item")
        self.assertTemplateUsed(response, "home.html")
