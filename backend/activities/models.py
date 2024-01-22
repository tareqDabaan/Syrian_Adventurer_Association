# Django imports 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from typing import Any

# Local modules imports
from users.managers import UserManager
from backend import settings

