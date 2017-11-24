# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth import get_user_model
from . import models

class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        # New user created
        user = User.objects.create(
            username="product_rating", password="prod_rating123")
        self.assertIsInstance(user.product_user, models.Product_User_Table)
        user.save()
        self.assertIsInstance(user.product_user, models.Product_User_Table)
