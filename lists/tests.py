from django.test import TestCase
from lists.models import Item


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


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_itmes(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")
