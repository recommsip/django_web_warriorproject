from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SimpleHomePageTest(TestCase):
    
    def setUp(self):
        # Create a user in the test database (same model used by Admin)
        self.username = 'admin_hero'
        self.password = 'SecretPass123!'
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password,
            email='admin@game.com'
        )
        
    def test_login_page_status_code(self):
        response = self.client.get(reverse('game:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/login.html')

    def test_successful_login(self):
        # Submit credentials to the login view
        response = self.client.post(reverse('game:login'), {
            'username': self.username,
            'password': self.password,
        }, follow=True)

        # Confirm the request redirected to tavern (200 after redirect)
        self.assertEqual(response.status_code, 200)
        
        # Confirm user is authenticated in the test session
        self.assertTrue(response.context['user'].is_authenticated)
    
    def test_character_select_page_status_code(self):
            url = reverse('game:boss')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
                
    def test_boss_list_status_code(self):
            url = reverse('game:boss_list')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
    
    def test_reset_page_status_code(self):
        # 1. Use 'game:encounter' (namespace:name) instead of 'encounter/'
        url = reverse('game:reset')
        
        # 2. Make the GET request
        response = self.client.get(url)
        
        # 3. Check status code
        self.assertEqual(response.status_code, 200)
        
    def test_boss_create_page_status_code(self):
            # 1. Use 'game:encounter' (namespace:name) instead of 'encounter/'
            url = reverse('game:boss_create')
            
            # 2. Make the GET request
            response = self.client.get(url)
            
            # 3. Check status code
            self.assertEqual(response.status_code, 200)

    # def test_encounter_page_uses_correct_template(self):
    #     # 1. Use the correct reverse name
    #     response = self.client.get(reverse('game:encounter'))
        
    #     # 2. Pass your actual HTML filename here (e.g., 'game/encounter.html' or 'encounter.html')
    #     self.assertTemplateUsed(response, 'encounter.html')
    
    