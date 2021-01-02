from datetime import date, time
from django.contrib.auth.models import User
from django.db import utils
from django.test import TestCase
from re import match
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import Query, Option, Attendee, Choice


class ModelRelationsTest(TestCase):
    def setUp(self):
        self.query = Query.objects.create(name='When can we meet?')
        self.options = [
                Option.objects.create(begin_date='2021-01-01', query=self.query),
                Option.objects.create(begin_date='2021-01-02', query=self.query),
                Option.objects.create(begin_date='2021-01-03', query=self.query), ]
        self.attendees = [
                Attendee.objects.create(name='Alisa'),
                Attendee.objects.create(name='Asisa'), ]
        self.choices = [
                Choice.objects.create(option=self.options[0], attendee=self.attendees[0], status='Y'),
                Choice.objects.create(option=self.options[1], attendee=self.attendees[0], status='N'),
                Choice.objects.create(option=self.options[2], attendee=self.attendees[0], status='Y'),
                Choice.objects.create(option=self.options[0], attendee=self.attendees[1], status='M'),
                Choice.objects.create(option=self.options[1], attendee=self.attendees[1], status='Y'),
                Choice.objects.create(option=self.options[2], attendee=self.attendees[1], status='Y'), ]

    def test_prerequisites(self):
        self.assertIsNotNone(self.query)
        self.assertEqual(len(self.options), 3)
        self.assertEqual(len(self.query.options.all()), 3)
        self.assertEqual(len(self.query.choices()), 6)

        self.assertEqual(len(self.attendees), 2)
        self.assertEqual(len(self.attendees[0].choices.all()), 3)
        self.assertEqual(len(self.attendees[0].choices.all()), 3)

        self.assertEqual(len(self.choices), 6)
        self.assertEqual(len(self.options[0].choices.all()), 2)
        self.assertEqual(len(self.options[1].choices.all()), 2)
        self.assertEqual(len(self.options[2].choices.all()), 2)

    def test_unique_choice(self):
        try:
            Choice.objects.create(option=self.options[0], attendee=self.attendees[0], status='M')
            self.fail
        except utils.IntegrityError:
            pass

    def test_delete_attendee_deletes_choices(self):
        self.assertEqual(len(self.query.choices()), 6)

        self.attendees[0].delete()
        self.assertEqual(len(self.query.choices()), 3)

        self.attendees[1].delete()
        self.assertEqual(len(self.query.choices()), 0)

    def test_delete_option_deletes_choices(self):
        self.assertEqual(len(self.query.choices()), 6)

        self.options[0].delete()
        self.assertEqual(len(self.query.choices()), 4)

        self.options[1].delete()
        self.assertEqual(len(self.query.choices()), 2)

        self.options[2].delete()
        self.assertEqual(len(self.query.choices()), 0)

    def test_delete_query_deletes_options_and_choices(self):
        self.assertEqual(len(self.query.options.all()), 3)
        self.assertEqual(len(self.query.choices()), 6)

        self.query.delete()

        self.assertEqual(len(Option.objects.all()), 0)
        self.assertEqual(len(Choice.objects.all()), 0)


class OptionModelTest(TestCase):
    def setUp(self):
        self.query = Query.objects.create(name='When can we meet?')
        self.option = Option.objects.create(begin_date='2021-01-01', query=self.query)

    def test_option_string(self):
        self.assertEqual(str(self.option), '2021-01-01 (When can we meet?)')
        self.option.begin_time = time(18, 00)
        self.assertEqual(str(self.option), '2021-01-01 18:00 (When can we meet?)')
        self.option.end_time = time(19, 00)
        self.assertEqual(str(self.option), '2021-01-01 18:00 - 19:00 (When can we meet?)')
        self.option.end_date = date(2021, 1, 2)
        self.option.end_time = time(3, 00)
        self.assertEqual(str(self.option), '2021-01-01 18:00 - 2021-01-02 03:00 (When can we meet?)')


class QueryApiAnonTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.query = Query.objects.create(name='When can we meet?')
        cls.options = [
                Option.objects.create(begin_date='2021-01-01', begin_time='18:00:00', end_date='2021-01-02', end_time='03:00:00', query=cls.query),
                Option.objects.create(begin_date='2021-01-02', begin_time='18:00:00', end_date='2021-01-03', end_time='03:00:00', query=cls.query),
                Option.objects.create(begin_date='2021-01-03', begin_time='18:00:00', end_date='2021-01-04', end_time='03:00:00', query=cls.query), ]
        cls.attendees = [
                Attendee.objects.create(name='Alisa'),
                Attendee.objects.create(name='Asisa'), 
                Attendee.objects.create(name='Takatuka'), ]
        cls.choices = [
                Choice.objects.create(option=cls.options[0], attendee=cls.attendees[0], status='Y'),
                Choice.objects.create(option=cls.options[1], attendee=cls.attendees[0], status='N'),
                Choice.objects.create(option=cls.options[2], attendee=cls.attendees[0], status='Y'),
                Choice.objects.create(option=cls.options[0], attendee=cls.attendees[1], status='M'),
                Choice.objects.create(option=cls.options[1], attendee=cls.attendees[1], status='Y'),
                Choice.objects.create(option=cls.options[2], attendee=cls.attendees[1], status='Y'), ]

    # root --------------------------------------------------------------------
    def test_get_root(self):
        response = self.client.get('/app/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['queries'])
        self.assertIsNotNone(json['options'])
        self.assertIsNotNone(json['choices'])
        self.assertIsNotNone(json['attendees'])
        self.assertTrue(match(r'^https?://[a-zA-Z-.]+/app/queries/\?format=json$', json['queries']))
        self.assertTrue(match(r'^https?://[a-zA-Z-.]+/app/options/\?format=json$', json['options']))
        self.assertTrue(match(r'^https?://[a-zA-Z-.]+/app/choices/\?format=json$', json['choices']))
        self.assertTrue(match(r'^https?://[a-zA-Z-.]+/app/attendees/\?format=json$', json['attendees']))

    def test_post_root(self):
        response = self.client.post('/app/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_root(self):
        response = self.client.put('/app/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_root(self):
        response = self.client.patch('/app/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_root(self):
        response = self.client.delete('/app/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_options_root(self):
        response = self.client.options('/app/', {'format': 'json'})
        self.assertEqual(response.status_code, 200)
        # TODO: implement me
        pass

    # query list --------------------------------------------------------------
    def test_get_query_list(self):
        response = self.client.get('/app/queries/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_query_list(self):
        response = self.client.post('/app/queries/', {'name': 'New Query'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertGreaterEqual(int(json['id']), 1)
        self.assertEqual(json['name'], 'New Query')
        self.assertEqual(json['options'], [])

    def test_put_query_list(self):
        response = self.client.put('/app/queries/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_query_list(self):
        response = self.client.patch('/app/queries/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_query_list(self):
        response = self.client.delete('/app/queries/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_options_query_list(self):
        response = self.client.options('/app/queries/', {'format': 'json'})
        self.assertEqual(response.status_code, 200)
        # TODO: implement me
        pass

    # query item --------------------------------------------------------------
    def test_get_query_item(self):
        response = self.client.get('/app/queries/' + str(self.query.id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['id'], self.query.id)
        self.assertEqual(json['name'], 'When can we meet?')

        self.assertEqual(len(json['options']), 3)

        self.assertEqual(json['options'][0]['id'], self.options[0].id)
        self.assertEqual(json['options'][1]['id'], self.options[1].id)
        self.assertEqual(json['options'][2]['id'], self.options[2].id)

        self.assertEqual(json['options'][0]['begin_date'], self.options[0].begin_date)
        self.assertEqual(json['options'][1]['begin_date'], self.options[1].begin_date)
        self.assertEqual(json['options'][2]['begin_date'], self.options[2].begin_date)

        self.assertEqual(json['options'][0]['begin_time'], self.options[0].begin_time)
        self.assertEqual(json['options'][1]['begin_time'], self.options[1].begin_time)
        self.assertEqual(json['options'][2]['begin_time'], self.options[2].begin_time)

        self.assertEqual(json['options'][0]['end_date'], self.options[0].end_date)
        self.assertEqual(json['options'][1]['end_date'], self.options[1].end_date)
        self.assertEqual(json['options'][2]['end_date'], self.options[2].end_date)

        self.assertEqual(json['options'][0]['end_time'], self.options[0].end_time)
        self.assertEqual(json['options'][1]['end_time'], self.options[1].end_time)
        self.assertEqual(json['options'][2]['end_time'], self.options[2].end_time)

        self.assertEqual(len(json['options'][0]['choices']), 2)
        self.assertEqual(len(json['options'][1]['choices']), 2)
        self.assertEqual(len(json['options'][2]['choices']), 2)

        self.assertEqual(json['options'][0]['choices'][0]['id'], self.choices[0].id)
        self.assertEqual(json['options'][0]['choices'][0]['attendee'], self.choices[0].attendee.name)
        self.assertEqual(json['options'][0]['choices'][0]['attendee_id'], self.choices[0].attendee.id)
        self.assertEqual(json['options'][0]['choices'][0]['status'], self.choices[0].status)
        self.assertEqual(json['options'][1]['choices'][0]['id'], self.choices[1].id)
        self.assertEqual(json['options'][1]['choices'][0]['attendee'], self.choices[1].attendee.name)
        self.assertEqual(json['options'][1]['choices'][0]['attendee_id'], self.choices[1].attendee.id)
        self.assertEqual(json['options'][1]['choices'][0]['status'], self.choices[1].status)
        self.assertEqual(json['options'][2]['choices'][0]['id'], self.choices[2].id)
        self.assertEqual(json['options'][2]['choices'][0]['attendee'], self.choices[2].attendee.name)
        self.assertEqual(json['options'][2]['choices'][0]['attendee_id'], self.choices[2].attendee.id)
        self.assertEqual(json['options'][2]['choices'][0]['status'], self.choices[2].status)
        self.assertEqual(json['options'][0]['choices'][1]['id'], self.choices[3].id)
        self.assertEqual(json['options'][0]['choices'][1]['attendee'], self.choices[3].attendee.name)
        self.assertEqual(json['options'][0]['choices'][1]['attendee_id'], self.choices[3].attendee.id)
        self.assertEqual(json['options'][0]['choices'][1]['status'], self.choices[3].status)
        self.assertEqual(json['options'][1]['choices'][1]['id'], self.choices[4].id)
        self.assertEqual(json['options'][1]['choices'][1]['attendee'], self.choices[4].attendee.name)
        self.assertEqual(json['options'][1]['choices'][1]['attendee_id'], self.choices[4].attendee.id)
        self.assertEqual(json['options'][1]['choices'][1]['status'], self.choices[4].status)
        self.assertEqual(json['options'][2]['choices'][1]['id'], self.choices[5].id)
        self.assertEqual(json['options'][2]['choices'][1]['attendee'], self.choices[5].attendee.name)
        self.assertEqual(json['options'][2]['choices'][1]['attendee_id'], self.choices[5].attendee.id)
        self.assertEqual(json['options'][2]['choices'][1]['status'], self.choices[5].status)

    def test_post_query_item(self):
        response = self.client.post('/app/queries/' + str(self.query.id) + '/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_query_item(self):
        response = self.client.put('/app/queries/' + str(self.query.id) + '/', {'name': 'New Query'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['id'], self.query.id)
        self.assertEqual(json['name'], 'New Query')

        self.assertEqual(len(json['options']), 3)

        self.assertEqual(json['options'][0]['id'], self.options[0].id)
        self.assertEqual(json['options'][1]['id'], self.options[1].id)
        self.assertEqual(json['options'][2]['id'], self.options[2].id)

        self.assertEqual(json['options'][0]['begin_date'], self.options[0].begin_date)
        self.assertEqual(json['options'][1]['begin_date'], self.options[1].begin_date)
        self.assertEqual(json['options'][2]['begin_date'], self.options[2].begin_date)

        self.assertEqual(json['options'][0]['begin_time'], self.options[0].begin_time)
        self.assertEqual(json['options'][1]['begin_time'], self.options[1].begin_time)
        self.assertEqual(json['options'][2]['begin_time'], self.options[2].begin_time)

        self.assertEqual(json['options'][0]['end_date'], self.options[0].end_date)
        self.assertEqual(json['options'][1]['end_date'], self.options[1].end_date)
        self.assertEqual(json['options'][2]['end_date'], self.options[2].end_date)

        self.assertEqual(json['options'][0]['end_time'], self.options[0].end_time)
        self.assertEqual(json['options'][1]['end_time'], self.options[1].end_time)
        self.assertEqual(json['options'][2]['end_time'], self.options[2].end_time)

        self.assertEqual(len(json['options'][0]['choices']), 2)
        self.assertEqual(len(json['options'][1]['choices']), 2)
        self.assertEqual(len(json['options'][2]['choices']), 2)

        self.assertEqual(json['options'][0]['choices'][0]['id'], self.choices[0].id)
        self.assertEqual(json['options'][0]['choices'][0]['attendee'], self.choices[0].attendee.name)
        self.assertEqual(json['options'][0]['choices'][0]['attendee_id'], self.choices[0].attendee.id)
        self.assertEqual(json['options'][0]['choices'][0]['status'], self.choices[0].status)
        self.assertEqual(json['options'][1]['choices'][0]['id'], self.choices[1].id)
        self.assertEqual(json['options'][1]['choices'][0]['attendee'], self.choices[1].attendee.name)
        self.assertEqual(json['options'][1]['choices'][0]['attendee_id'], self.choices[1].attendee.id)
        self.assertEqual(json['options'][1]['choices'][0]['status'], self.choices[1].status)
        self.assertEqual(json['options'][2]['choices'][0]['id'], self.choices[2].id)
        self.assertEqual(json['options'][2]['choices'][0]['attendee'], self.choices[2].attendee.name)
        self.assertEqual(json['options'][2]['choices'][0]['attendee_id'], self.choices[2].attendee.id)
        self.assertEqual(json['options'][2]['choices'][0]['status'], self.choices[2].status)
        self.assertEqual(json['options'][0]['choices'][1]['id'], self.choices[3].id)
        self.assertEqual(json['options'][0]['choices'][1]['attendee'], self.choices[3].attendee.name)
        self.assertEqual(json['options'][0]['choices'][1]['attendee_id'], self.choices[3].attendee.id)
        self.assertEqual(json['options'][0]['choices'][1]['status'], self.choices[3].status)
        self.assertEqual(json['options'][1]['choices'][1]['id'], self.choices[4].id)
        self.assertEqual(json['options'][1]['choices'][1]['attendee'], self.choices[4].attendee.name)
        self.assertEqual(json['options'][1]['choices'][1]['attendee_id'], self.choices[4].attendee.id)
        self.assertEqual(json['options'][1]['choices'][1]['status'], self.choices[4].status)
        self.assertEqual(json['options'][2]['choices'][1]['id'], self.choices[5].id)
        self.assertEqual(json['options'][2]['choices'][1]['attendee'], self.choices[5].attendee.name)
        self.assertEqual(json['options'][2]['choices'][1]['attendee_id'], self.choices[5].attendee.id)
        self.assertEqual(json['options'][2]['choices'][1]['status'], self.choices[5].status)

    def test_patch_query_item(self):
        response = self.client.patch('/app/queries/' + str(self.query.id) + '/', {'name': 'Updated Query'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['id'], self.query.id)
        self.assertEqual(json['name'], 'Updated Query')

        self.assertEqual(len(json['options']), 3)

        self.assertEqual(json['options'][0]['id'], self.options[0].id)
        self.assertEqual(json['options'][1]['id'], self.options[1].id)
        self.assertEqual(json['options'][2]['id'], self.options[2].id)

        self.assertEqual(json['options'][0]['begin_date'], self.options[0].begin_date)
        self.assertEqual(json['options'][1]['begin_date'], self.options[1].begin_date)
        self.assertEqual(json['options'][2]['begin_date'], self.options[2].begin_date)

        self.assertEqual(json['options'][0]['begin_time'], self.options[0].begin_time)
        self.assertEqual(json['options'][1]['begin_time'], self.options[1].begin_time)
        self.assertEqual(json['options'][2]['begin_time'], self.options[2].begin_time)

        self.assertEqual(json['options'][0]['end_date'], self.options[0].end_date)
        self.assertEqual(json['options'][1]['end_date'], self.options[1].end_date)
        self.assertEqual(json['options'][2]['end_date'], self.options[2].end_date)

        self.assertEqual(json['options'][0]['end_time'], self.options[0].end_time)
        self.assertEqual(json['options'][1]['end_time'], self.options[1].end_time)
        self.assertEqual(json['options'][2]['end_time'], self.options[2].end_time)

        self.assertEqual(len(json['options'][0]['choices']), 2)
        self.assertEqual(len(json['options'][1]['choices']), 2)
        self.assertEqual(len(json['options'][2]['choices']), 2)

        self.assertEqual(json['options'][0]['choices'][0]['id'], self.choices[0].id)
        self.assertEqual(json['options'][0]['choices'][0]['attendee'], self.choices[0].attendee.name)
        self.assertEqual(json['options'][0]['choices'][0]['attendee_id'], self.choices[0].attendee.id)
        self.assertEqual(json['options'][0]['choices'][0]['status'], self.choices[0].status)
        self.assertEqual(json['options'][1]['choices'][0]['id'], self.choices[1].id)
        self.assertEqual(json['options'][1]['choices'][0]['attendee'], self.choices[1].attendee.name)
        self.assertEqual(json['options'][1]['choices'][0]['attendee_id'], self.choices[1].attendee.id)
        self.assertEqual(json['options'][1]['choices'][0]['status'], self.choices[1].status)
        self.assertEqual(json['options'][2]['choices'][0]['id'], self.choices[2].id)
        self.assertEqual(json['options'][2]['choices'][0]['attendee'], self.choices[2].attendee.name)
        self.assertEqual(json['options'][2]['choices'][0]['attendee_id'], self.choices[2].attendee.id)
        self.assertEqual(json['options'][2]['choices'][0]['status'], self.choices[2].status)
        self.assertEqual(json['options'][0]['choices'][1]['id'], self.choices[3].id)
        self.assertEqual(json['options'][0]['choices'][1]['attendee'], self.choices[3].attendee.name)
        self.assertEqual(json['options'][0]['choices'][1]['attendee_id'], self.choices[3].attendee.id)
        self.assertEqual(json['options'][0]['choices'][1]['status'], self.choices[3].status)
        self.assertEqual(json['options'][1]['choices'][1]['id'], self.choices[4].id)
        self.assertEqual(json['options'][1]['choices'][1]['attendee'], self.choices[4].attendee.name)
        self.assertEqual(json['options'][1]['choices'][1]['attendee_id'], self.choices[4].attendee.id)
        self.assertEqual(json['options'][1]['choices'][1]['status'], self.choices[4].status)
        self.assertEqual(json['options'][2]['choices'][1]['id'], self.choices[5].id)
        self.assertEqual(json['options'][2]['choices'][1]['attendee'], self.choices[5].attendee.name)
        self.assertEqual(json['options'][2]['choices'][1]['attendee_id'], self.choices[5].attendee.id)
        self.assertEqual(json['options'][2]['choices'][1]['status'], self.choices[5].status)

    def test_delete_query_item(self):
        response = self.client.delete('/app/queries/' + str(self.query.id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/app/queries/' + str(self.query.id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_options_query_item(self):
        response = self.client.options('/app/queries/' + str(self.query.id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: implement me
        pass

    # option list -------------------------------------------------------------
    def test_get_option_list(self):
        response = self.client.get('/app/options/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_option_list(self):
        response = self.client.post('/app/options/', {
            'query_id': self.query.id,
            'begin_date': '2021-01-01', 'begin_time': '18:00:00',
            'end_date': '2021-01-02', 'end_time': '03:00:00'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertGreaterEqual(int(json['id']), 1)
        self.assertEqual(json['query_id'], self.query.id)
        self.assertEqual(json['begin_date'], '2021-01-01')
        self.assertEqual(json['begin_time'], '18:00:00')
        self.assertEqual(json['end_date'], '2021-01-02')
        self.assertEqual(json['end_time'], '03:00:00')

    def test_put_option_list(self):
        response = self.client.put('/app/options/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_option_list(self):
        response = self.client.patch('/app/options/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_option_list(self):
        response = self.client.delete('/app/options/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_options_option_list(self):
        response = self.client.options('/app/options/', {'format': 'json'})
        self.assertEqual(response.status_code, 200)
        # TODO: implement me
        pass

    # option item -------------------------------------------------------------
    def test_get_option_item(self):
        response = self.client.get('/app/options/' + str(self.options[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['id'], self.options[0].id)
        self.assertEqual(json['query_id'], self.options[0].query.id)
        self.assertEqual(json['begin_date'], self.options[0].begin_date)
        self.assertEqual(json['begin_time'], self.options[0].begin_time)
        self.assertEqual(json['end_date'], self.options[0].end_date)
        self.assertEqual(json['end_time'], self.options[0].end_time)

    def test_post_option_item(self):
        response = self.client.post('/app/options/' + str(self.options[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_option_item(self):
        response = self.client.put('/app/options/' + str(self.options[0].id) + '/', {
            'query_id': self.query.id,
            'begin_date': '2021-01-11', 'begin_time': '20:30:00',
            'end_date': '2021-01-11', 'end_time': '21:00:00'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(int(json['id']), self.options[0].id)
        self.assertEqual(json['query_id'], self.query.id)
        self.assertEqual(json['begin_date'], '2021-01-11')
        self.assertEqual(json['begin_time'], '20:30:00')
        self.assertEqual(json['end_date'], '2021-01-11')
        self.assertEqual(json['end_time'], '21:00:00')

    def test_patch_option_item(self):
        response = self.client.patch('/app/options/' + str(self.options[0].id) + '/', {
            'begin_time': '18:30:00'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(int(json['id']), self.options[0].id)
        self.assertEqual(json['query_id'], self.query.id)
        self.assertEqual(json['begin_date'], '2021-01-01')
        self.assertEqual(json['begin_time'], '18:30:00')
        self.assertEqual(json['end_date'], '2021-01-02')
        self.assertEqual(json['end_time'], '03:00:00')
        pass

    def test_delete_option_item(self):
        response = self.client.delete('/app/options/' + str(self.options[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/app/options/' + str(self.options[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_options_option_item(self):
        response = self.client.options('/app/options/' + str(self.options[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: implement me
        pass

    # choice list -------------------------------------------------------------
    def test_get_choice_list(self):
        response = self.client.get('/app/choices/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_choice_list(self):
        response = self.client.post('/app/choices/', {
            'option_id': self.options[0].id,
            'attendee_id': self.attendees[2].id,
            'status': 'Y'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertGreaterEqual(int(json['id']), 1)
        self.assertEqual(int(json['option_id']), self.options[0].id)
        self.assertEqual(int(json['attendee_id']), self.attendees[2].id)
        self.assertEqual(json['attendee'], self.attendees[2].name)
        self.assertEqual(json['status'], 'Y')

    def test_put_choice_list(self):
        response = self.client.put('/app/choices/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_choice_list(self):
        response = self.client.patch('/app/choices/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_choice_list(self):
        response = self.client.delete('/app/choices/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_choices_option_list(self):
        response = self.client.options('/app/options/', {'format': 'json'})
        self.assertEqual(response.status_code, 200)
        # TODO: implement me
        pass

    # choice item -------------------------------------------------------------
    def test_get_choice_item(self):
        response = self.client.get('/app/choices/' + str(self.choices[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(int(json['id']), self.choices[0].id)
        self.assertEqual(int(json['option_id']), self.choices[0].option_id)
        self.assertEqual(int(json['attendee_id']), self.choices[0].attendee_id)
        self.assertEqual(json['attendee'], self.choices[0].attendee.name)
        self.assertEqual(json['status'], self.choices[0].status)

    def test_post_choice_item(self):
        response = self.client.post('/app/choices/' + str(self.choices[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_choice_item(self):
        response = self.client.put('/app/choices/' + str(self.choices[0].id) + '/', {
            'option_id': self.options[1].id,
            'attendee_id': self.attendees[2].id,
            'status': 'N'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(int(json['id']), self.choices[0].id)
        self.assertEqual(int(json['option_id']), self.options[1].id)
        self.assertEqual(int(json['attendee_id']), self.attendees[2].id)
        self.assertEqual(json['attendee'], self.attendees[2].name)
        self.assertEqual(json['status'], 'N')

    def test_patch_choice_item(self):
        response = self.client.patch('/app/choices/' + str(self.choices[0].id) + '/', {
            'status': 'N'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(int(json['id']), self.choices[0].id)
        self.assertEqual(int(json['option_id']), self.options[0].id)
        self.assertEqual(int(json['attendee_id']), self.attendees[0].id)
        self.assertEqual(json['attendee'], self.attendees[0].name)
        self.assertEqual(json['status'], 'N')

    def test_delete_choice_item(self):
        response = self.client.delete('/app/choices/' + str(self.choices[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/app/choices/' + str(self.choices[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_choices_option_item(self):
        response = self.client.options('/app/choices/' + str(self.choices[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: implement me

    # # attendee list -------------------------------------------------------------
    def test_get_attendee_list(self):
        response = self.client.get('/app/attendees/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_attendee_list(self):
        response = self.client.post('/app/attendees/', {
            'name': 'new attendee'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertGreaterEqual(int(json['id']), 1)
        self.assertEqual(json['name'], 'new attendee')

    def test_put_attendee_list(self):
        response = self.client.put('/app/attendees/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_attendee_list(self):
        response = self.client.patch('/app/attendees/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_attendee_list(self):
        response = self.client.delete('/app/attendees/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_attendees_option_list(self):
        response = self.client.options('/app/options/', {'format': 'json'})
        self.assertEqual(response.status_code, 200)
        # TODO: implement me

    # attendee item -------------------------------------------------------------
    def test_get_attendee_item(self):
        response = self.client.get('/app/attendees/' + str(self.attendees[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(json['id'], self.attendees[0].id)
        self.assertEqual(json['name'], self.attendees[0].name)

    def test_post_attendee_item(self):
        response = self.client.post('/app/attendees/' + str(self.attendees[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_attendee_item(self):
        response = self.client.put('/app/attendees/' + str(self.attendees[0].id) + '/', {
            'name': 'new attendee'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(int(json['id']), self.attendees[0].id)
        self.assertEqual(json['name'], 'new attendee')

    def test_patch_attendee_item(self):
        response = self.client.patch('/app/attendees/' + str(self.attendees[0].id) + '/', {
            'name': 'new attendee'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json = response.json()
        self.assertIsNotNone(json)

        self.assertEqual(int(json['id']), self.attendees[0].id)
        self.assertEqual(json['name'], 'new attendee')

    def test_delete_attendee_item(self):
        response = self.client.delete('/app/attendees/' + str(self.attendees[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/app/attendees/' + str(self.attendees[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_attendees_option_item(self):
        response = self.client.options('/app/attendees/' + str(self.options[0].id) + '/', {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: implement me


class APIAuthTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
         User.objects.create_user(
                 'testuser', 'test@email.com', 'testpassword')

    def setUp(self):
        token_response = self.client.post('/app/auth-token/', {
                'username': 'testuser', 'password': 'testpassword', })
        self.assertEqual(token_response.status_code, 200)
        json = token_response.json()
        token = json['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_something(self):
        pass
