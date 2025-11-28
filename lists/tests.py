import unittest

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
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

        # always redirect after a post (traditional ssr site)
        self.assertRedirects(response, "/")
    
    @unittest.expectedFailure
    def test_can_save_multiple_items(self):
        # test via http layer, not db-like methods given in ItemModelTest
        # won't work at present
        self.client.post("/", data={"item_text": "first item"})
        response = self.client.post("/", data={"item_text": "second item"})
        self.assertContains(response, "first item")
        self.assertContains(response, "second item")


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

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)
