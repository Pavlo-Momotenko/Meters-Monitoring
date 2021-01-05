import unittest
from django.test.runner import DiscoverRunner
from django.urls import reverse

from meter import views
from django.test import TestCase
from meter import models


class MeterTestCase(TestCase):
    def setUp(self):
        models.Meter.objects.create(name='First', unit='one')
        models.Meter.objects.create(name='Second', unit='two')

    def test_vars(self):
        first = models.Meter.objects.get(name='First')
        second = models.Meter.objects.get(name='Second')
        self.assertEqual(first.name, 'First')
        self.assertEqual(second.name, 'Second')


class ViewTest(TestCase):
    def setUp(self):
        models.Meter.objects.create(name='First', unit='one')
        models.Meter.objects.create(name='Second', unit='two')

    def test_new_meter_view(self):
        response = self.client.get('/new_meter/')
        self.assertEqual(response.status_code, 200)

    def test_index_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_list_meters(self):
        response = self.client.get('/meter/2/')
        self.assertEqual(response.status_code, 200)
