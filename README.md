# Paw & Care
Paw & Care is a Django-based web application designed to manage a pet care business efficiently. It focuses on providing veterinary services and efficient clinic management. It serves as a digital solution for pet clinics to streamline operations, ensuring effective management of client relationships, medical records, and financial transactions.

## Features
This application allows only Registered Users to use and users must log in before accessing this web application. This application allows users to add or edit new data:
- **Owner Management**: Store and manage details about pet owners, such as name, address, phone, and email.  
- **Pet Management**: Track pet information, including species, breed, date of birth, gender, and weight.  
- **Veterinarian Management**: Record veterinarian details like specialization, license number, and contact information.  
- **Appointment Scheduling**: Schedule appointments with veterinarians, including appointment time, reason, and status tracking.  
- **Medical Records**: Keep detailed medical records, including diagnoses, treatments, and prescribed medications.  
- **Billing System**: Record payments for appointments with the total amount, payment status (paid, pending, overdue), and method (credit card, cash, bank transfer).
- **Statistics Page**: Show statistics about Individual Statistics, Clinic Statistics, Appointment Statistics, Billing & Payment Analysis. Users can not edit this page.

## Database Schema
![image](https://github.com/user-attachments/assets/7357c2a5-9583-48eb-9649-930c7042ef71)
#### 1. `users`
- Purpose: Stores user account information for authentication and access.
- Columns:
    - `user_id` (int): Unique identifier for each user (Primary Key).
    - `username` (varchar(100)): The username for login.
    - `password` (varchar(100)): Encrypted or hashed password for authentication.

#### 2. `owners`
- Purpose: Keeps information about pet owners.
- Columns:
  - `owner_id` (int): Unique identifier for each pet owner (Primary Key).
  - `first_name` (varchar(100)): Owner's first name.
  - `last_name` (varchar(100)): Owner's last name.
  - `address` (text): Address of the owner.
  - `phone_number` (varchar(15)): Contact number of the owner.
  - `email` (varchar(255)): Email address of the owner.
  - `registration_date` (datetime): The date and time the owner registered.

#### 3. `pets`
- Purpose: Stores detailed information about pets.
- Columns:
  - `pet_id` (int): Unique identifier for each pet (Primary Key).
  - `owner_id` (int): Links to the owner of the pet (Foreign Key).
  - `name` (varchar(255)): Name of the pet.
  - `species` (varchar(50)): Type of animal (e.g., dog, cat).
  - `breed` (varchar(100)): Breed of the pet.
  - `date_of_birth` (date): Birthdate of the pet.
  - `gender` (varchar(10)): Gender of the pet.
  - `weight` (decimal(5,2)): Weight of the pet.

#### 4. `veterinarians`
- Purpose: Stores information about veterinarians.
- Columns:
  - `vet_id` (int): Unique identifier for each veterinarian (Primary Key).
  - `first_name` (varchar(100)): Veterinarian's first name.
  - `last_name` (varchar(100)): Veterinarian's last name.
  - `specialization` (varchar(255)): Area of expertise (e.g., surgery, dermatology).
  - `license_number` (varchar(50)): Professional license number.
  - `phone_number` (varchar(15)): Contact number.
  - `email` (varchar(255)): Email address.

#### 5. `appointments`
- Purpose: Tracks appointments scheduled for pets.
- Columns:
  - `appointment_id` (int): Unique identifier for each appointment (Primary Key).
  - `pet_id` (int): Links to the pet for this appointment (Foreign Key).
  - `owner_id` (int): Links to the owner of the pet (Foreign Key).
  - `vet_id` (int): Links to the veterinarian assigned to the appointment (Foreign Key).
  - `appointment_date` (date): The date of the appointment.
  - `appointment_time` (time): The time of the appointment.
  - `reason` (text): The reason for the appointment.
  - `status` (varchar(20)): Status of the appointment (e.g., completed, cancelled).

#### 6. `medical_records`
- Purpose: Stores medical records for pets.
- Columns:
  - `record_id` (int): Unique identifier for each medical record (Primary Key).
  - `appointment_id` (int): Links to the associated appointment (Foreign Key).
  - `pet_id` (int): Links to the pet being treated (Foreign Key).
  - `vet_id` (int): Links to the veterinarian responsible (Foreign Key).
  - `visit_date` (datetime): Date of the medical visit.
  - `diagnosis` (text): Diagnosis information.
  - `treatment` (text): Treatment details.
  - `prescribed_medication` (varchar(255)): Medications prescribed during the visit.
  - `notes` (text): Additional notes about the visit.

#### 7. `billing`
- Purpose: Handles billing and payment details for appointments.
- Columns:
  - `bill_id` (int): Unique identifier for each bill (Primary Key).
  - `appointment_id` (int): Links to the associated appointment (Foreign Key).
  - `total_amount` (decimal(10,2)): Total amount to be paid.
  - `payment_status` (varchar(20)): Status of the payment (e.g., paid, unpaid).
  - `payment_method` (varchar(20)): Method of payment (e.g., cash, credit card).
  - `payment_date` (datetime): The date and time of payment.

Here is the presentation slide: [Presentation](https://github.com/user-attachments/files/17942688/Paw.Care.pdf)

## Requirements
Required Python and Django packages are listed in [requirements.txt](./requirements.txt).

## Installation the Application
Read and follow the instructions in [Installation the Application](Installation.md).

## Running the Application
1. Start the server in the virtual environment. <br>
  Activate the virtualenv for this project
   * On Windows:
   ``` 
   venv\Scripts\activate
   ```
   * On macOS and Linux:
   ``` 
   source venv/bin/activate
   ```
   Start the django server:
   ```
   python manage.py runserver
   ```
   This starts a web server listening on port 8000.

2. You should see this message printed in the terminal window:
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```
   If you get a message that the port is unavailable, then run the server on a different port (1024 thru 65535) such as:
   ```
   python manage.py runserver 12345
   ```

2. In a web browser, navigate to <http://localhost:8000>

3. To stop the server, press CTRL-C in the terminal window. Exit the virtual environment by closing the window or by typing:
   ```
   deactivate
   ```

## Demo User Accounts
* `admin` password `admin`

## Our Members
| Name                      | Responsibilities                                  | Github
|---------------------------|--------------------------------------------------| --------------------------------------------------
| Phumrapee CHAOWANAPRICHA  | Implement `Edit` feature, Implement project model          | [PhumrapeeC](https://github.com/PhumrapeeC)
| Atikarn KRUAYKRIANGKRAI   | Implement UI for all pages, `Search` feature, Data table (Home page) | [Nanokwok](https://github.com/Nanokwok)
| Thorung BOONKAEW          | Implement Statistic page, Add new data features  | [thorungb](https://github.com/thorungb)
| Nicha RUANGRIT            | Design the database schema, SQL query, and Presentation Slide | [nicharr-nn](https://github.com/nicharr-nn)

## Thank you for your attention
