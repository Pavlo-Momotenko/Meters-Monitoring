# Meters Monitoring

(Python, Django)

## Review

1. Main page without meters:
   ![Main page image](./readme_imgs/1.png)

2. Create meter page:
   ![Create meter page](./readme_imgs/2.png)

3. Completed form on create meter page:
   ![Completed form](./readme_imgs/3.png)

4. Just created new meter:
   ![New one meter](./readme_imgs/4.png)

5. Created 3 meters for example:
   ![Created 3 meters](./readme_imgs/5.png)

6. Model Meter has a constraint unique, so if you will try to create a meter with the same name, you will get error
   message:
   ![Error message](./readme_imgs/6.png)

7. Meter details page without statistic data:
   ![Meter details image](./readme_imgs/7.png)

8. Meter details after uploading data in `.csv` file:
   ![Meter details after uploading](./readme_imgs/8.png)

9. Also, you can add new data or update previous by loading `*.csv` files with data:
   ![Edited meter graph](./readme_imgs/9.png)

10. If your file contain some unsuitable data that should not be added in the meter, you will see an alert with error explanation. Errors divided on one-line error and errors with additional details:

11. If you need to remove all meter data, you should press `Reset` button:
    ![Removed meter data](./readme_imgs/10.png)

12. You can delete a meter on using `Delete` button that located aside:
    ![3 meters](./readme_imgs/11.png)
    ![Arrow image](./readme_imgs/13.png)
    ![2 meters](./readme_imgs/12.png)
    
13. The project has customized error pages, for example 404 error page:


## Launching

1. Clone this repository.
2. Install requirements: [`requirements.txt`][requirements-location]. You can use pip `pip install -r requirements.txt`.
3. Create database schema `create database meter_project;`.
4. Manage settings in [`settings.py`][settings-location]:
   `DATABASES = {
   'default': {
   'ENGINE': 'django.db.backends.mysql',
   'NAME': 'meter_project',
   'USER': 'root',
   'PASSWORD': '12345' } }`
   
5. Enjoy!

## Testing

To launch business logic test cases type `python manage.py test` in command line.


[requirements-location]: ./requirements.txt

[settings-location]: ./djangoTestProject/settings.py