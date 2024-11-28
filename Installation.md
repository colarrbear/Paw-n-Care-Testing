# Installation the Application

### Clone or Download code from Github

You can clone the repository using this command:
   ``` 
   git clone https://github.com/Nanokwok/Paw-n-Care.git
   ```

### Create a virtual environment and install dependencies
1. Change directory to the application:
   ``` 
   cd Paw-n-Care
   ```
2. Create a virtual environment by running the following command:
   ``` 
   python -m venv venv
   ```
3. Activate the virtual environment
   * On Windows:
        ``` 
        venv\Scripts\activate
        ```
    * On macOS and Linux:
        ``` 
        source venv/bin/activate
        ```
4. Install Dependencies for required python modules:
    ``` 
    pip install -r requirements.txt
    ```

### Run migrations
Run migrations to apply database migrations:
  ``` 
  python manage.py migrate
  ```

### Install data from the data fixtures
  ``` 
  python manage.py loaddata paw_n_care\data\pets.json paw_n_care\data\owners.json paw_n_care\data\veterinarians.json paw_n_care\data\users.json paw_n_care\data\appointments.json paw_n_care\data\medical_records.json paw_n_care\data\billings.json
  ```

More detailt of how to running the application is in [readme.md](README.md)