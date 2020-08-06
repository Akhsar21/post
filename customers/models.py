from django.db import models

# Create your models here.


class Customer(models.Model):
    company_name = models.CharField(max_length=220)
    budget = models.PositiveIntegerField()
    employment = models.PositiveIntegerField()
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

    def __unicode__(self):
        return self.company_name
