import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'database_project.settings')

import django

django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.utils import timezone

import time
import datetime

from paw_n_care.models import Owner, Pet, Veterinarian, Appointment, \
    MedicalRecord, Billing, User


@override_settings(DEBUG=True)
class PawNCareSeleniumTests(StaticLiveServerTestCase):
    """Selenium tests for the Paw N Care application."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up Chrome WebDriver
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Run in headless mode (no UI)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.service = ChromeService(ChromeDriverManager().install())
        cls.browser = webdriver.Chrome(service=cls.service,
                                       options=chrome_options)
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        """Set up test data for each test."""
        # Create test veterinarian
        self.vet = Veterinarian.objects.create(
            first_name='John',
            last_name='Doe',
            specialization='General',
            license_number='VET12345',
            phone_number='555-123-4567',
            email='john.doe@pawcare.com'
        )

        # Create test owner
        self.owner = Owner.objects.create(
            first_name='Jane',
            last_name='Smith',
            address='123 Main St, Anytown',
            phone_number='555-987-6543',
            email='jane.smith@example.com',
            registration_date=timezone.now()
        )

        # Create test pet
        self.pet = Pet.objects.create(
            owner=self.owner,
            name='Buddy',
            species='dog',
            breed='labrador',
            date_of_birth=timezone.now().date() - datetime.timedelta(
                days=365 * 2),  # 2 years old
            gender='Male',
            weight=25.5
        )

        # Create test appointment
        self.appointment = Appointment.objects.create(
            pet=self.pet,
            owner=self.owner,
            vet=self.vet,
            appointment_date=timezone.now().date() + datetime.timedelta(
                days=7),
            appointment_time=timezone.now().time(),
            reason='Annual checkup',
            status='Scheduled'
        )

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be visible on the page."""
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def test_login(self):
        """Test user login functionality."""
        # Test Case ID: TC01 - Login with correct info

        # Step 1: Navigate to login page
        self.browser.get(f'{self.live_server_url}')

        try:
            # Step 2-3: Enter valid credentials
            username_input = self.wait_for_element(By.XPATH,
                                                   '//*[@id="login-form"]/div/div/div[3]/div/input')
            password_input = self.wait_for_element(By.XPATH,
                                                   '//*[@id="login-form"]/div/div/div[4]/div/input')

            username_input.send_keys('doctor1')
            password_input.send_keys('doctor1')

            # Step 4: Click login button
            submit_button = self.wait_for_element(By.XPATH,
                                                  '//*[@id="login-form"]/div/div/button')
            submit_button.click()

        except TimeoutException as e:
            self.fail(f"Login test failed - element not found: {str(e)}")

    def test_login_with_incorrect_info(self):
        """Test user login with incorrect credentials."""
        # Test Case ID: TC02 - Login with incorrect info

        # Step 1: Navigate to login page
        self.browser.get(f'{self.live_server_url}')

        try:
            # Step 2: Enter invalid credentials (valid username but invalid password)
            username_input = self.wait_for_element(By.XPATH,
                                                   '//*[@id="login-form"]/div/div/div[3]/div/input')
            password_input = self.wait_for_element(By.XPATH,
                                                   '//*[@id="login-form"]/div/div/div[4]/div/input')

            username_input.send_keys('doctor1')
            password_input.send_keys('wrongpassword')

            # Step 3: Click login button
            submit_button = self.wait_for_element(By.XPATH,
                                                  '//*[@id="login-form"]/div/div/button')
            submit_button.click()

            # Wait for error message to appear
            error_message = self.wait_for_element(By.CSS_SELECTOR,
                                                  '.alert-danger',
                                                  timeout=5)

            # Verify expected result
            self.assertTrue(error_message.is_displayed(),
                            "Error message should be displayed")
            self.assertIn('login', self.browser.current_url,
                          "User should remain on login page")

        except TimeoutException as e:
            self.fail(
                f"Login with incorrect info test failed - element not found: {str(e)}")