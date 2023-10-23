# How to setup repo
- Clone the repo
- Make sure `python` and `poetry` are installed
- Run `poetry install` to install dependencies
- Run `poetry shell` to activate the virtual environment
- `cd` into `src` directory
- apply migrations by running `python manage.py migrate`
- Create a superuser by running `python manage.py createsuperuser`

# How to run tests
- `cd` into `src` directory
- Run `python manage.py test`


# How to run the API
- (optional) Make sure you `.env` has `NUTRITIONIX_CLIENT_ID` and `NUTRITIONIX_API_KEY` set
- `cd` into `src` directory
- Run `python manage.py runserver`
- fire up your browser and go to `http://127.0.0.1:8000/`
