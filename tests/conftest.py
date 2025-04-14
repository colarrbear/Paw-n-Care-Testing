# import os
# import pytest
# import django
# from django.conf import settings
#
#
# def pytest_configure():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE',
#                           'database_project.settings')
#     try:
#         # Initialize Django
#         django.setup()
#     except ModuleNotFoundError as e:
#         if "tailwind" in str(e):
#             # Temporarily remove tailwind from INSTALLED_APPS if not installed
#             settings.INSTALLED_APPS = [
#                 app for app in settings.INSTALLED_APPS
#                 if app != 'tailwind'
#             ]
#             django.setup()
#         else:
#             raise
#
#     # Configure test settings
#     settings.DEBUG = True
#     settings.STATIC_URL = '/static/'
#
#     # Use SQLite for testing
#     settings.DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': ':memory:',
#         }
#     }
#
#
# @pytest.fixture(scope='session')
# def django_db_setup():
#     """Ensure tests use the test database"""
#     pass
#
#
# @pytest.fixture
# def browser():
#     from selenium import webdriver
#     from webdriver_manager.chrome import ChromeDriverManager
#     from selenium.webdriver.chrome.options import Options
#
#     options = Options()
#     # options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#
#     browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#     browser.implicitly_wait(10)
#     yield browser
#     browser.quit()

def pytest_configure():
    from django.conf import settings
    import django

    # Only configure settings if they aren't already configured
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            # You might need to add other Django settings here
            DJANGO_SETTINGS_MODULE='database_project.settings',
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'django.contrib.sessions',
                # Your app
                'paw_n_care',
            ],
            SECRET_KEY='dummy-key-for-tests',
        )
        django.setup()
