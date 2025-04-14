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

    # def test_login(self):
    #     """Test user login functionality."""
    #     # Test Case ID: TC01 - Login with correct info
    #
    #     # Step 1: Navigate to login page
    #     self.browser.get(f'{self.live_server_url}')
    #
    #     try:
    #         # Step 2-3: Enter valid credentials
    #         username_input = self.wait_for_element(By.XPATH,
    #                                                '//*[@id="login-form"]/div/div/div[3]/div/input')
    #         password_input = self.wait_for_element(By.XPATH,
    #                                                '//*[@id="login-form"]/div/div/div[4]/div/input')
    #
    #         username_input.send_keys('doctor1')
    #         password_input.send_keys('doctor1')
    #
    #         # Step 4: Click login button
    #         submit_button = self.wait_for_element(By.XPATH,
    #                                               '//*[@id="login-form"]/div/div/button')
    #         submit_button.click()
    #
    #     except TimeoutException as e:
    #         self.fail(f"Login test failed - element not found: {str(e)}")

    # def test_login_with_incorrect_info(self):
    #     """Test user login with incorrect credentials."""
    #     # Test Case ID: TC02 - Login with incorrect info
    #
    #     # Step 1: Navigate to login page
    #     self.browser.get(f'{self.live_server_url}')
    #
    #     try:
    #         # Step 2: Enter invalid credentials (valid username but invalid password)
    #         username_input = self.wait_for_element(By.XPATH,
    #                                                '//*[@id="login-form"]/div/div/div[3]/div/input')
    #         password_input = self.wait_for_element(By.XPATH,
    #                                                '//*[@id="login-form"]/div/div/div[4]/div/input')
    #
    #         username_input.send_keys('doctor1')
    #         password_input.send_keys('wrongpassword')
    #
    #         # Step 3: Click login button
    #         submit_button = self.wait_for_element(By.XPATH,
    #                                               '//*[@id="login-form"]/div/div/button')
    #         submit_button.click()
    #
    #         # Wait for error message to appear
    #         error_message = self.wait_for_element(By.CSS_SELECTOR,
    #                                               '.alert-danger',
    #                                               timeout=5)
    #
    #         # Verify expected result
    #         self.assertTrue(error_message.is_displayed(),
    #                         "Error message should be displayed")
    #         self.assertIn('login', self.browser.current_url,
    #                       "User should remain on login page")
    #
    #     except TimeoutException as e:
    #         self.fail(
    #             f"Login with incorrect info test failed - element not found: {str(e)}")

    # def test_create_new_owner(self):
    #     """Test creating a new owner with valid information."""
    #     # Test Case ID: TC03 - Create new owner
    #
    #     # First login as staff
    #     self.browser.get(f'{self.live_server_url}')
    #
    #     try:
    #         # Login (using your existing login test as base)
    #         username_input = self.wait_for_element(By.XPATH,
    #                                                '//*[@id="login-form"]/div/div/div[3]/div/input')
    #         password_input = self.wait_for_element(By.XPATH,
    #                                                '//*[@id="login-form"]/div/div/div[4]/div/input')
    #         username_input.send_keys('doctor1')  # Using existing credentials
    #         password_input.send_keys('doctor1')
    #
    #         submit_button = self.wait_for_element(By.XPATH,
    #                                               '//*[@id="login-form"]/div/div/button')
    #         submit_button.click()
    #
    #         # Wait for dashboard to load and navigate to appointments page
    #         appointments_link = self.wait_for_element(By.LINK_TEXT,
    #                                                   'appointments')
    #         appointments_link.click()
    #
    #         # Scroll down to owner section
    #         self.browser.execute_script(
    #             "window.scrollTo(0, document.body.scrollHeight)")
    #
    #         # Click "Add a new owner" button
    #         add_owner_btn = self.wait_for_element(By.XPATH, '//*[@id="addNewOwnerBtn"]')
    #         add_owner_btn.click()
    #
    #         # Fill in owner information
    #         test_owner_data = {
    #             'first_name': 'NewTest',
    #             'last_name': 'Owner',
    #             'address': '456 Test Street',
    #             'phone_number': '555-123-7890',
    #             'email': 'newtest@example.com'
    #         }
    #
    #         self.wait_for_element(By.NAME, 'first_name').send_keys(
    #             test_owner_data['first_name'])
    #         self.browser.find_element(By.NAME, 'last_name').send_keys(
    #             test_owner_data['last_name'])
    #         self.browser.find_element(By.NAME, 'address').send_keys(
    #             test_owner_data['address'])
    #         self.browser.find_element(By.NAME, 'phone').send_keys(
    #             test_owner_data['phone_number'])
    #         self.browser.find_element(By.NAME, 'email').send_keys(
    #             test_owner_data['email'])
    #
    #         # Submit the form (this would typically be part of the appointment submission)
    #         # For testing owner creation, we can verify the data was entered correctly
    #         submit_button = self.wait_for_element(By.XPATH,
    #                                               '//*[@id="owner-form"]/div/div/div/div[5]/button')
    #         submit_button.click()
    #
    #         # Verify the owner was created in the database
    #         created_owner = Owner.objects.filter(last_name='Owner').first()
    #         self.assertIsNotNone(created_owner, "Owner should exist in database")
    #         self.assertEqual(created_owner.email, test_owner_data['email'])
    #
    #         # Verify the owner appears in the dropdown if we switch to "Choose existing owner"
    #         choose_owner_btn = self.wait_for_element(By.ID, 'chooseOwnerBtn')
    #         choose_owner_btn.click()
    #
    #         owner_dropdown = self.wait_for_element(By.NAME, 'existing_owner')
    #         self.assertIn('NewTest Owner', owner_dropdown.text,
    #                       "New owner should appear in dropdown")
    #
    #     except TimeoutException as e:
    #         self.fail(
    #             f"Create new owner test failed - element not found: {str(e)}")

    def test_update_owner_info(self):
        """Test updating owner information."""
        # Test Case ID: TC04 - Update owner info

        # First login as staff
        self.browser.get(f'{self.live_server_url}')

        try:
            # Login (using existing credentials)
            username_input = self.wait_for_element(By.XPATH,
                                                   '//*[@id="login-form"]/div/div/div[3]/div/input')
            password_input = self.wait_for_element(By.XPATH,
                                                   '//*[@id="login-form"]/div/div/div[4]/div/input')
            username_input.send_keys('doctor1')
            password_input.send_keys('doctor1')

            # Navigate to owners page
            self.browser.get(f'{self.live_server_url}/home/owner/')

            # Find the edit button for our test owner (Jane Smith)
            edit_buttons = self.browser.find_elements(By.LINK_TEXT, 'Edit')
            for button in edit_buttons:
                if str(self.owner.owner_id) in button.get_attribute('href'):
                    button.click()
                    break

            # Update owner information
            updated_data = {
                'first_name': 'Jane Updated',
                'last_name': 'Smith Updated',
                'address': '456 Updated St, Newtown',
                'phone_number': '555-111-2222',
                'email': 'jane.updated@example.com'
            }

            # Clear and fill the form fields
            first_name = self.wait_for_element(By.NAME, 'first_name')
            first_name.clear()
            first_name.send_keys(updated_data['first_name'])

            last_name = self.browser.find_element(By.NAME, 'last_name')
            last_name.clear()
            last_name.send_keys(updated_data['last_name'])

            address = self.browser.find_element(By.NAME, 'address')
            address.clear()
            address.send_keys(updated_data['address'])

            phone = self.browser.find_element(By.NAME, 'phone')
            phone.clear()
            phone.send_keys(updated_data['phone_number'])

            email = self.browser.find_element(By.NAME, 'email')
            email.clear()
            email.send_keys(updated_data['email'])

            # Submit the form
            # submit_button = self.browser.find_element(By.XPATH,
            #                                       '//*[@id="owner-form"]/div/div/div/div[5]/button')
            submit_button = self.wait_for_element(By.CSS_SELECTOR,
                                                  'button[type="submit"]')
            submit_button.click()

            # Verify the data in the database
            updated_owner = Owner.objects.get(owner_id=self.owner.owner_id)
            self.assertEqual(updated_owner.first_name,
                             updated_data['first_name'])
            self.assertEqual(updated_owner.last_name,
                             updated_data['last_name'])
            self.assertEqual(updated_owner.address, updated_data['address'])
            self.assertEqual(updated_owner.phone_number,
                             updated_data['phone_number'])
            self.assertEqual(updated_owner.email, updated_data['email'])

        except TimeoutException as e:
            self.fail(
                f"Update owner info test failed - element not found: {str(e)}")

