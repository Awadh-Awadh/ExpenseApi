from pydoc import describe
from django.db import models
from authentication.models import CustomUser

class Income(models.Model):

  CATEGORIES = (

    ("SALARY", "SALARY"),
    ("SIDE_HUSTLE", "SIDE_HUSTLE"),
    ("COMMISIONS", "COMMISIONS"),
    ("OTHE", "OTHE")

  )

  categories = models.CharField(choices=CATEGORIES, max_length=255)
  owner=models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=7, decimal_places=2)
  description = models.TextField()
  date = models.DateField(blank=False, null=True)

  class Meta:
      ordering = ['-date']


  def __str__(self):
    return f"{str(self.owner)}'s Income"