from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e@jj4fiw5&t_k1rq^2-yr+%qc5d276c1lyanwpv-oanq^x8@oc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass

