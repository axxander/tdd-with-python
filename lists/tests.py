import unittest

from bs4 import BeautifulSoup
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
        soup = BeautifulSoup(response.content, "html.parser")

        form = soup.find("form", {"method": "POST", "action": "/"})
        self.assertIsNotNone(form)

        # assertContains does simple substring formatting, so it will
        #  include newlines, spaces, tabs etc. So we are just going to use
        #  two assertions for now
        self.assertContains(response, '<input')
        self.assertContains(response, 'name="item_text"')

    def test_can_save_a_POST_request(self):
        self.client.post("/", data={"item_text": "A new list item"})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")


    def test_redirects_after_POST(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")
    
    @unittest.expectedFailure
    def test_can_save_multiple_items(self):
        # test via http layer, not db-like methods given in ItemModelTest
        # won't work at present
        self.client.post("/", data={"item_text": "first item"})
        response = self.client.post("/", data={"item_text": "second item"})
        self.assertContains(response, "first item")
        self.assertContains(response, "second item")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_renders_input_form(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        soup = BeautifulSoup(response.content, "html.parser")

        form = soup.find("form", {"method": "POST", "action": "/"})
        self.assertIsNotNone(form)

        inputbox = soup.find("input", {"name": "item_text"})
        self.assertIsNotNone(inputbox)
        
    def test_displays_all_list_items(self):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")


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
