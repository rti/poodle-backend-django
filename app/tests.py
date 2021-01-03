from django.test import TestCase
from rest_framework.test import APITestCase
from re import match

from django.contrib.auth.models import User
from app.models import Item


class ItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Item.objects.create(name='An Item')

    def test_find_brand_by_name(self):
        item = Item.objects.get(name='An Item')
        self.assertEqual(item.name, 'An Item')

    def test_find_fails_for_non_existing_items(self):
        try:
            Item.objects.get(name='Another Item')
            self.fail
        except Item.DoesNotExist:
            pass


class ItemAPIAnonTest(APITestCase):
    items = []

    @classmethod
    def setUpTestData(cls):
        cls.items = [
                Item.objects.create(name='An Item'),
                Item.objects.create(name='Another Item'),
                Item.objects.create(name='Again an Item'),
                ]

    def test_get_root_with_items_reference(self):
        response = self.client.get('/app/', {'format': 'json'})
        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['items'])
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/\?format=json$',
            json['items']))

    def test_get_item_json(self):
        response = self.client.get(
                '/app/items/' + str(self.items[0].id) + '/',
                {'format': 'json'})
        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['id'], self.items[0].id)
        self.assertEqual(json['name'], 'An Item')
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/' +
            str(self.items[0].id) + r'/\?format=json$', json['url']))

    def test_get_items_list(self):
        response = self.client.get('/app/items/', {'format': 'json'})
        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json)
        self.assertEqual(len(json), 3)

        sorted_json = sorted(json, key=lambda i: i['id'])

        self.assertEqual(sorted_json[0]['id'], self.items[0].id)
        self.assertEqual(sorted_json[0]['name'], 'An Item')
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/' +
            str(self.items[0].id) + r'/\?format=json$',
            sorted_json[0]['url']))

        self.assertEqual(sorted_json[1]['id'], self.items[1].id)
        self.assertEqual(sorted_json[1]['name'], 'Another Item')
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/' +
            str(self.items[1].id) + r'/\?format=json$',
            sorted_json[1]['url']))

        self.assertEqual(sorted_json[2]['id'], self.items[2].id)
        self.assertEqual(sorted_json[2]['name'], 'Again an Item')
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/' +
            str(self.items[2].id) + r'/\?format=json$',
            sorted_json[2]['url']))


class ItemAPIAuthTest(APITestCase):
    items = []

    @classmethod
    def setUpTestData(cls):
        cls.items = [
                Item.objects.create(name='An Item'),
                Item.objects.create(name='Another Item'),
                Item.objects.create(name='Again an Item'),
                ]

        User.objects.create_user(
                'testuser', 'test@email.com', 'testpassword')

    def setUp(self):
        token_response = self.client.post('/app/auth-token/', {
            'username': 'testuser',
            'password': 'testpassword',
            })
        self.assertEqual(token_response.status_code, 200)
        json = token_response.json()
        token = json['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_get_root_with_items_reference(self):
        response = self.client.get('/app/', {'format': 'json'})
        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['items'])
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/\?format=json$',
            json['items']))

    def test_get_item_json(self):
        response = self.client.get(
                '/app/items/' + str(self.items[0].id) + '/',
                {'format': 'json'})
        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['id'], self.items[0].id)
        self.assertEqual(json['name'], 'An Item')
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/' +
            str(self.items[0].id) + r'/\?format=json$', json['url']))

    def test_get_items_list(self):
        response = self.client.get('/app/items/', {'format': 'json'})
        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json)
        self.assertEqual(len(json), 3)

        sorted_json = sorted(json, key=lambda i: i['id'])

        self.assertEqual(sorted_json[0]['id'], self.items[0].id)
        self.assertEqual(sorted_json[0]['name'], 'An Item')
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/' +
            str(self.items[0].id) + r'/\?format=json$',
            sorted_json[0]['url']))

        self.assertEqual(sorted_json[1]['id'], self.items[1].id)
        self.assertEqual(sorted_json[1]['name'], 'Another Item')
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/' +
            str(self.items[1].id) + r'/\?format=json$',
            sorted_json[1]['url']))

        self.assertEqual(sorted_json[2]['id'], self.items[2].id)
        self.assertEqual(sorted_json[2]['name'], 'Again an Item')
        self.assertTrue(match(
            r'^https?://[a-zA-Z-.]+/app/items/' +
            str(self.items[2].id) + r'/\?format=json$',
            sorted_json[2]['url']))

    def test_create_item_json(self):
        response = self.client.post('/app/items/', {
                'name': 'New Item',
            }, format='json')
        self.assertEqual(response.status_code, 201)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['name'], 'New Item')

    def test_create_item_without_name_json(self):
        response = self.client.post('/app/items/', {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_put_item_json(self):
        response = self.client.post('/app/items/', {
                'name': 'An Item', }, format='json')
        self.assertEqual(response.status_code, 201)

        json = response.json()
        self.assertIsNotNone(json)
        created_id = json['id']

        response = self.client.put('/app/items/' + str(created_id) + '/', {
                'name': 'Completely new Item', }, format='json')
        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['name'], 'Completely new Item')

    def test_update_patch_item_json(self):
        response = self.client.post('/app/items/', {
                'name': 'An Item', }, format='json')
        self.assertEqual(response.status_code, 201)

        json = response.json()
        self.assertIsNotNone(json)
        created_id = json['id']

        response = self.client.patch(
                '/app/items/' + str(created_id) + '/', {
                    'name': 'Updated Item'}, format='json')
        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['name'], 'Updated Item')

    def test_delete_item(self):
        response = self.client.post('/app/items/', {
                'name': 'Item',
            }, format='json')
        self.assertEqual(response.status_code, 201)

        json = response.json()
        self.assertIsNotNone(json)
        created_id = json['id']

        response = self.client.delete(
                '/app/items/' + str(created_id) + '/', format='json')
        self.assertEqual(response.status_code, 204)

    def test_delete_item_not_existing(self):
        response = self.client.delete('/app/items/99999/', format='json')
        self.assertEqual(response.status_code, 404)
