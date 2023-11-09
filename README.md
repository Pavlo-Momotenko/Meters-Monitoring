# Meters Monitoring

(Python, Django, MySQL)

## Launching

1. Clone this repository.
2. Install requirements: `pip install -r requirements.txt`
3. Create MySQL database `create database meters_monitoring;`
4. Change settings in [`settings.py`][settings-location] if needed: 
   ```
   DATABASES = {
      "default": {
         "ENGINE": "django.db.backends.mysql",
         "HOST": "127.0.0.1",
         "NAME": "meters_monitoring",
         "USER": "root",
         "PASSWORD": "12345",
      }
   }
   ```
5. Run server: `python manage.py runserver`

[settings-location]: MetersMonitoring/settings.py