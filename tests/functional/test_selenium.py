import os

from django.core.management import call_command
from django.utils.dateparse import parse_datetime

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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

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

    @staticmethod
    def load_data():
        """Load initial data for the tests."""
        # Load test data into the database
        call_command('loaddata', 'paw_n_care/data/users.json')
        call_command('loaddata', 'paw_n_care/data/veterinarians.json')
        call_command('loaddata', 'paw_n_care/data/owners.json')
        call_command('loaddata', 'paw_n_care/data/pets.json')
        call_command('loaddata', 'paw_n_care/data/appointments.json')
        call_command('loaddata', 'paw_n_care/data/medical_records.json')
        call_command('loaddata', 'paw_n_care/data/billings.json')

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

    def test_create_new_owner(self):
        """Test creating a new owner with valid information."""
        # Test Case ID: TC03 - Create new owner

        # First login as staff
        self.browser.get(f'{self.live_server_url}')

        try:
            # Login (using your existing login test as base)
            username_input = self.wait_for_element(By.XPATH,
                                                   '//*[@id="login-form"]/div/div/div[3]/div/input')
            password_input = self.wait_for_element(By.XPATH,
                                                   '//*[@id="login-form"]/div/div/div[4]/div/input')
            username_input.send_keys('doctor1')  # Using existing credentials
            password_input.send_keys('doctor1')

            submit_button = self.wait_for_element(By.XPATH,
                                                  '//*[@id="login-form"]/div/div/button')
            submit_button.click()

            # Wait for dashboard to load and navigate to appointments page
            appointments_link = self.wait_for_element(By.LINK_TEXT, 'appointments')
            appointments_link.click()

            # Wait for appointments page to load
            # self.wait_for_element(By.XPATH,
            #                       '//div[contains(text(), "Add appointment")]')

            # Scroll down to owner section
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)")

            # Click "Add a new owner" button
            add_owner_btn = self.wait_for_element(By.XPATH, '//*[@id="addNewOwnerBtn"]')
            add_owner_btn.click()

            # Fill in owner information
            test_owner_data = {
                'first_name': 'NewTest',
                'last_name': 'Owner',
                'address': '456 Test Street',
                'phone_number': '555-123-7890',
                'email': 'newtest@example.com'
            }

            self.wait_for_element(By.NAME, 'first_name').send_keys(
                test_owner_data['first_name'])
            self.browser.find_element(By.NAME, 'last_name').send_keys(
                test_owner_data['last_name'])
            self.browser.find_element(By.NAME, 'address').send_keys(
                test_owner_data['address'])
            self.browser.find_element(By.NAME, 'phone').send_keys(
                test_owner_data['phone_number'])
            self.browser.find_element(By.NAME, 'email').send_keys(
                test_owner_data['email'])

            # Submit the form (this would typically be part of the appointment submission)
            # For testing owner creation, we can verify the data was entered correctly

            # Verify the owner was created in the database
            created_owner = Owner.objects.filter(last_name='Owner').first()
            self.assertIsNotNone(created_owner, "Owner should exist in database")
            self.assertEqual(created_owner.email, test_owner_data['email'])

            # Verify the owner appears in the dropdown if we switch to "Choose existing owner"
            choose_owner_btn = self.wait_for_element(By.ID, 'chooseOwnerBtn')
            choose_owner_btn.click()

            owner_dropdown = self.wait_for_element(By.NAME, 'existing_owner')
            self.assertIn('NewTest Owner', owner_dropdown.text,
                          "New owner should appear in dropdown")

        except TimeoutException as e:
            self.fail(
                f"Create new owner test failed - element not found: {str(e)}")

    def test_TC10_update_medical_record(self):
        """Test updating an existing medical record."""
        # Test Case ID: TC10 - Update medical record
        from datetime import datetime

        try:
            # Step 1: Login first
            self.browser.get(f'{self.live_server_url}/')
            username_input = self.wait_for_element(By.NAME, 'username')
            password_input = self.wait_for_element(By.NAME, 'password')
            username_input.send_keys('doctor1')
            password_input.send_keys('doctor1')
            password_input.send_keys(Keys.RETURN)
            time.sleep(1)

            # Step 2: Create a medical record to update
            # Find an appointment without a medical record
            available_appointment = Appointment.objects.exclude(
                appointment_id__in=MedicalRecord.objects.values_list('appointment_id', flat=True)
            ).first()
            
            if not available_appointment:
                self.fail("No available appointments for medical record creation")
            
            # Navigate to medical records creation form
            self.browser.get(f'{self.live_server_url}/medical-records/')
            time.sleep(1)

            # Fill the form to create a medical record
            select = Select(self.wait_for_element(By.NAME, 'appointment_id'))
            for option in select.options:
                if str(available_appointment.appointment_id) in option.text:
                    option.click()
                    break
            
            # Set visit date
            visit_date_str = datetime.now().strftime('%Y-%m-%dT%H:%M')
            visit_date = self.wait_for_element(By.NAME, 'visit_date')
            visit_date.clear()
            self.browser.execute_script(
                "arguments[0].value = arguments[1];",
                visit_date,
                visit_date_str
            )
            
            # Set initial values - store these to verify they change
            initial_diagnosis = 'Arthritis'
            initial_treatment = 'Joint Supplements'
            initial_medication = 'Non-steroidal anti-inflammatory drugs (NSAIDs)'
            initial_notes = 'Initial notes for TC10 test'
            
            # Use dropdowns properly
            Select(self.wait_for_element(By.NAME, 'diagnosis')).select_by_visible_text(initial_diagnosis)
            Select(self.wait_for_element(By.NAME, 'treatment')).select_by_visible_text(initial_treatment)
            Select(self.wait_for_element(By.NAME, 'prescribed_medication')).select_by_visible_text(initial_medication)
            
            notes_input = self.wait_for_element(By.NAME, 'notes')
            notes_input.clear()
            notes_input.send_keys(initial_notes)
            
            # Submit the form to create the medical record
            submit_btn = self.wait_for_element(By.XPATH, 
                '//*[@id="medical-records-form"]/div/div/div/div/div[2]/button')
            submit_btn.click()
            time.sleep(2)
            
            # Step 3: Find the newly created medical record
            # Get the latest medical record from the database
            medical_record = MedicalRecord.objects.latest('record_id')
            
            # Step 4: Navigate to the edit page for the medical record
            self.browser.get(f'{self.live_server_url}/home/edit/medical-record/{medical_record.record_id}/')
            time.sleep(2)
            
            # Step 5: Update the fields
            new_diagnosis = 'Allergies'
            new_treatment = 'Antihistamines'
            new_medication = 'Immunosuppressive Medications'
            new_notes = 'Updated notes for TC10 test'
            
            # Clear and update diagnosis
            diagnosis_field = self.wait_for_element(By.NAME, 'diagnosis')
            diagnosis_field.clear()
            diagnosis_field.send_keys(new_diagnosis)
            
            # Clear and update treatment
            treatment_field = self.wait_for_element(By.NAME, 'treatment')
            treatment_field.clear()
            treatment_field.send_keys(new_treatment)
            
            # Clear and update medication
            medication_field = self.wait_for_element(By.NAME, 'prescribed_medication')
            medication_field.clear()
            medication_field.send_keys(new_medication)
            
            # Clear and update notes
            notes_field = self.wait_for_element(By.NAME, 'notes')
            notes_field.clear()
            notes_field.send_keys(new_notes)
            
            # Step 6: Submit the form to update the record
            # Find the submit button - try multiple approaches
            try:
                submit_btn = self.browser.find_element(By.XPATH, 
                    '//*[@id="medical-records-form"]/div/div/div/div/div[2]/div[4]/button')
            except:
                try:
                    submit_btn = self.browser.find_element(By.CSS_SELECTOR, 
                        '#medical-records-form button[type="submit"]')
                except:
                    # Try to find any button in the form
                    submit_btn = self.browser.find_element(By.CSS_SELECTOR, 
                        '#medical-records-form button')
            
            # Screenshot before submitting for debugging
            self.browser.save_screenshot(f"update_med_record_before_submit_{medical_record.record_id}.png")
            
            # Submit the form
            submit_btn.click()
            time.sleep(2)
            
            # Step 7: Navigate back to the edit page to verify changes
            self.browser.get(f'{self.live_server_url}/home/edit/medical-record/{medical_record.record_id}/')
            time.sleep(2)
            
            # Step 8: Verify the fields were updated
            updated_diagnosis = self.wait_for_element(By.NAME, 'diagnosis').get_attribute('value')
            updated_treatment = self.wait_for_element(By.NAME, 'treatment').get_attribute('value')
            updated_medication = self.wait_for_element(By.NAME, 'prescribed_medication').get_attribute('value')
            updated_notes = self.wait_for_element(By.NAME, 'notes').get_attribute('value')
            
            # Take a screenshot of the verification page
            self.browser.save_screenshot(f"update_med_record_verification_{medical_record.record_id}.png")
            
            # Assert that the fields were updated correctly
            self.assertEqual(updated_diagnosis, new_diagnosis, 
                f"Diagnosis not updated. Expected '{new_diagnosis}', got '{updated_diagnosis}'")
            self.assertEqual(updated_treatment, new_treatment, 
                f"Treatment not updated. Expected '{new_treatment}', got '{updated_treatment}'")
            self.assertEqual(updated_medication, new_medication, 
                f"Medication not updated. Expected '{new_medication}', got '{updated_medication}'")
            self.assertEqual(updated_notes, new_notes, 
                f"Notes not updated. Expected '{new_notes}', got '{updated_notes}'")
            
            print(f"Successfully updated medical record {medical_record.record_id}")

        except TimeoutException as e:
            self.browser.save_screenshot("TC10_timeout_error.png")
            print(f"Current URL at error: {self.browser.current_url}")
            print(f"Page source at error:\n{self.browser.page_source[:2000]}")
            self.fail(f"TC10 failed - element not found: {str(e)}")
        except Exception as e:
            self.browser.save_screenshot("TC10_general_error.png")
            print(f"Current URL at error: {self.browser.current_url}")
            print(f"Page source at error:\n{self.browser.page_source[:2000]}")
            self.fail(f"TC10 failed with error: {str(e)}")

    def test_TC11_view_medical_record_details(self):
        """Test viewing medical record details."""
        # Test Case ID: TC11 - View medical record details
        from datetime import datetime

        try:
            # Step 1: Create a medical record to view
            visit_date_initial = timezone.now()
            medical_record = MedicalRecord.objects.create(
                appointment=self.appointment,
                vet=self.vet,
                pet=self.pet,
                visit_date=visit_date_initial,
                diagnosis='Diabetes',
                treatment='Insulin Therapy',
                prescribed_medication='Insulin Injections',
                notes='Needs regular checkups'
            )
            
            # Step 2: Login
            self.browser.get(f'{self.live_server_url}/')
            username_input = self.wait_for_element(By.NAME, 'username')
            password_input = self.wait_for_element(By.NAME, 'password')
            username_input.send_keys('doctor1')
            password_input.send_keys('doctor1')
            password_input.send_keys(Keys.RETURN)
            time.sleep(1)

            # Step 3: Navigate to medical record details page
            self.browser.get(f'{self.live_server_url}/home/edit/medical-record/{medical_record.record_id}/')
            time.sleep(2)
            
            # Take a screenshot for debugging
            self.browser.save_screenshot(f"view_medical_record_{medical_record.record_id}.png")
            
            # Step 4: Verify the medical record details are displayed correctly
            diagnosis = self.wait_for_element(By.NAME, 'diagnosis').get_attribute('value')
            treatment = self.wait_for_element(By.NAME, 'treatment').get_attribute('value')
            prescribed_medication = self.wait_for_element(By.NAME, 'prescribed_medication').get_attribute('value')
            notes = self.wait_for_element(By.NAME, 'notes').get_attribute('value')
            
            # Verify the details match what we created
            self.assertEqual(diagnosis, 'Diabetes', 
                f"Diagnosis mismatch. Expected 'Diabetes', got '{diagnosis}'")
            self.assertEqual(treatment, 'Insulin Therapy', 
                f"Treatment mismatch. Expected 'Insulin Therapy', got '{treatment}'")
            self.assertEqual(prescribed_medication, 'Insulin Injections', 
                f"Medication mismatch. Expected 'Insulin Injections', got '{prescribed_medication}'")
            self.assertEqual(notes, 'Needs regular checkups', 
                f"Notes mismatch. Expected 'Needs regular checkups', got '{notes}'")
            
            print(f"Successfully viewed medical record {medical_record.record_id}")
            
        except TimeoutException as e:
            self.browser.save_screenshot("TC11_timeout_error.png")
            print(f"Current URL at error: {self.browser.current_url}")
            print(f"Page source at error:\n{self.browser.page_source[:2000]}")
            self.fail(f"TC11 failed - element not found: {str(e)}")
        except Exception as e:
            self.browser.save_screenshot("TC11_general_error.png")
            print(f"Current URL at error: {self.browser.current_url}")
            print(f"Page source at error:\n{self.browser.page_source[:2000]}")
            self.fail(f"TC11 failed with error: {str(e)}")

    def test_TC12_create_billing(self):
        """Test creating a new billing record."""
        # Test Case ID: TC12 - Create billing

        try:
            self.test_login()

            # Navigate directly to billing creation page
            self.browser.get(f'{self.live_server_url}/billing/')

            # Select our test appointment
            appointment_select = self.wait_for_element(By.NAME, 'appointment_id')
            appointment_select.send_keys('Appointment ID: 1 Maximus by Dr.Chayakarn')

            # Enter billing details
            amount_input = self.wait_for_element(By.NAME, 'total_amount')
            amount_input.send_keys('500')

            payment_status = self.wait_for_element(By.NAME, 'payment_status')
            payment_status.send_keys('Pending')

            payment_method = self.wait_for_element(By.NAME, 'payment_method')
            payment_method.send_keys('Credit Card')

            # Set payment date to today
            today = timezone.now().strftime('%Y-%m-%dT%H:%M')
            payment_date = self.wait_for_element(By.NAME, 'payment_date')
            payment_date.send_keys(today)

            # Submit form
            submit_btn = self.wait_for_element(By.XPATH, '//*[@id="billing-form"]/div/div/div/div/button')
            submit_btn.click()

        except TimeoutException as e:
            self.fail(f"TC12 failed - element not found: {str(e)}")

    def test_TC13_update_payment_status(self):
        """Test updating payment status."""
        # Test Case ID: TC13 - Update payment status

        # Create a billing record first
        billing = Billing.objects.create(
            appointment=self.appointment,
            total_amount=300,
            payment_status='Pending',
            payment_method='Cash',
            payment_date=timezone.now()
        )

        try:
            self.test_login()

            # Navigate to billing home
            self.browser.get(f'{self.live_server_url}/home/billing/')

            # Click edit on our test billing record
            edit_btn = self.wait_for_element(
                By.XPATH, f'//a[@href="/home/edit/billing/{billing.bill_id}/"]')
            edit_btn.click()

            # Update payment status
            status_select = self.wait_for_element(By.NAME, 'payment_status')
            status_select.send_keys('Paid')

            # Submit form
            submit_btn = self.wait_for_element(By.XPATH, '//*[@id="billing-form"]/div/div/div/div/div[7]/button')
            submit_btn.click()

            # Verify the status was updated
            self.browser.get(f'http://127.0.0.1:8000/home/edit/billing/{billing.bill_id}/')
            updated_status = self.wait_for_element(By.NAME, 'payment_status').get_attribute('value')
            self.assertEqual(updated_status, 'Paid')

        except TimeoutException as e:
            self.fail(f"TC13 failed - element not found: {str(e)}")
