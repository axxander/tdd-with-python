import unittest

from bs4 import BeautifulSoup
from django.test import TestCase

from lists.models import Item, List


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

        form = soup.find("form", {"method": "POST", "action": "/lists/new"})
        self.assertIsNotNone(form)

        # assertContains does simple substring formatting, so it will
        #  include newlines, spaces, tabs etc. So we are just going to use
        #  two assertions for now
        self.assertContains(response, '<input')
        self.assertContains(response, 'name="item_text"')
    
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
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_renders_input_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        soup = BeautifulSoup(response.content, "html.parser")

        form = soup.find("form", {"method": "POST", "action": f"/lists/{mylist.id}/add_item"})
        self.assertIsNotNone(form)

        inputbox = soup.find("input", {"name": "item_text"})
        self.assertIsNotNone(inputbox)
        
    def test_displays_all_list_items(self):
        mylist = List.objects.create()
        Item.objects.create(text="itemey 1", list=mylist)
        Item.objects.create(text="itemey 2", list=mylist)
        other_list = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"/lists/{mylist.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item")

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new list item")
    
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{new_list.id}/")
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_itmes(self):
        mylist = List()
        mylist.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = mylist
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, mylist)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, mylist)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, mylist)

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)
