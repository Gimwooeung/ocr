from django.db import models

# Create your models here.
class DrugName(models.Model):
    drug_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'drug_name'