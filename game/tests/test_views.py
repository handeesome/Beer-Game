from django.test import TestCase, Client
from django.urls import reverse
from game.models import *

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('player', 'player@gmail.com', 'beergame123')
        self.userprofile = UserProfile.objects.create(user=self.user, is_instructor=False)
        self.client.login(username='player', password='beergame123')
        

    def test_home(self):
        response = self.client.get(reverse('game:home'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/main.html')

    # New test cases
    def test_register(self):
        responce = self.client.get(reverse('game:register'), follow=True)
        self.assertEquals(responce.status_code, 200)

    def test_login(self):
        responce = self.client.get(reverse('game:login'), follow=True)
        self.assertEquals(responce.status_code, 200)

    def test_logout(self):
        responce = self.client.get(reverse('game:logout'), follow=True)
        self.assertEquals(responce.status_code, 200)

    def test_accountSettings(self):
        response = self.client.get(reverse('game:accountSettings'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/accountSettings.html')

    def test_create_game(self):
        responce = self.client.get(reverse('game:create_game'), follow=True)
        self.assertEquals(responce.status_code, 200)

    def test_join(self):
        response = self.client.get(reverse('game:join'), follow=True)
        self.assertEquals(response.status_code, 200)