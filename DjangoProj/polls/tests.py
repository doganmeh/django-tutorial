import datetime
from django.utils.timezone import make_aware

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from polls import models


def get_url(app, model, action, kwargs=None):
    if kwargs is None:
        kwargs = {}
    url_name = app + ":" + model + "-" + action
    return reverse(url_name, kwargs=kwargs)


class TestGenericViews(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
    
    @classmethod
    def setUpTestData(cls):
        cls.app_name = 'polls'
        cls.model_name = 'question'
        # a_time = make_aware(datetime.datetime(2013, 11, 20, 20, 9, 26, 423063))
        cls.obj = models.Question.objects.create(
            **{
                'question_text': 'What grade are you?',
                'pub_date'     : make_aware(datetime.datetime.now()),
            }
        )
        cls.right_data = {
            'question_text': 'How old are you?',
            'pub_date'     : '2020-01-30 12:22',
        }
        cls.wrong_data = [
            {'pub_date': '2020-01-30 12:22'},
            {'question_text': 'How old are you?'},
        ]
    
    def setUp(self):
        settings.DEBUG = True  # somehow django has DEBUG=False by default for tests
        # self.client.login(username='testuser', password='t11111111')
    
    def test_get_create(self):
        url = get_url(self.app_name, self.model_name, "create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_create_success(self):
        create_url = get_url(self.app_name, self.model_name, "create")
        list_url = get_url(self.app_name, self.model_name, "list")
        url = create_url + '?next=' + list_url
        response = self.client.post(url, self.right_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, list_url)

    def test_post_create_failure(self):
        create_url = get_url(self.app_name, self.model_name, "create")
    
        if not isinstance(self.wrong_data, list):
            self.wrong_data = [self.wrong_data]
    
        for wd in self.wrong_data:
            wd['pk'] = self.obj.pk  # create
            response = self.client.post(create_url, wd)
            self.assertEqual(response.status_code, 200)
            self.assertIn('This field is required', str(response.content))

    def test_get_update(self):
        url = get_url(self.app_name, self.model_name, "update", kwargs={'pk': self.obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_update_success(self):
        update_url = get_url(self.app_name, self.model_name, "update", kwargs={'pk': self.obj.pk})
        list_url = get_url(self.app_name, self.model_name, "list")
        self.right_data['pk'] = self.obj.pk  # update
        url = update_url + '?next=' + list_url
        response = self.client.post(url, self.right_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, list_url)

    def test_post_update_failure(self):
        update_url = get_url(self.app_name, self.model_name, "update", kwargs={'pk': self.obj.pk})
        
        if not isinstance(self.wrong_data, list):
            self.wrong_data = [self.wrong_data]
        
        for wd in self.wrong_data:
            wd['pk'] = self.obj.pk  # update
            response = self.client.post(update_url, wd)
            self.assertEqual(response.status_code, 200)
            self.assertIn('This field is required', str(response.content))
    
    def test_get_delete(self):
        delete_url = get_url(self.app_name, self.model_name, "delete", kwargs={'pk': self.obj.pk})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        delete_url = get_url(self.app_name, self.model_name, "delete", kwargs={'pk': self.obj.pk})
        list_url = get_url(self.app_name, self.model_name, "list")
        url = delete_url + '?next=' + list_url
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, list_url)

    def test_get_detail(self):
        url = get_url(self.app_name, self.model_name, "detail", kwargs={'pk': self.obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('detail', str(response.content).lower())
    
    def test_get_list(self):
        url = get_url(self.app_name, self.model_name, "list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('list', str(response.content).lower())
