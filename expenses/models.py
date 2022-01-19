from turtle import ondrag
from django.db import models
from authentication.models import CustomUser
# Create your models here.


class Expenses(models.Model):

    CATEGOIES_EXPENSE = (

      ("ONLINE", "ONLINE"),
      ("TRAVE", "TRAVEL"),
      ("EXECUTIVE", "EXECUTIVE"),
      ("PREMIUM", "PREMIUM"),
      ("BASIC", "BASIC"),
      ("MIDDLE", "MIDDLE")
    )
    categories = models.CharField(choices=CATEGOIES_EXPENSE, max_length=255)
    amount=models.DecimalField(decimal_places=2, max_digits=5)
    owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    date=models.DateField(blank=False, null=False)
