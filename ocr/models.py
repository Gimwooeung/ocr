from django.db import models

# Create your models here.
class DrugName(models.Model):
    drug_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'drug_name'

class ContraindicatedDrug(models.Model):
    ingredient_a = models.CharField(max_length=255)
    ingredient_code_a = models.CharField(max_length=50)
    product_name_a = models.CharField(max_length=255)
    company_a = models.CharField(max_length=255)
    ingredient_b = models.CharField(max_length=255, null=True, blank=True)
    ingredient_code_b = models.CharField(max_length=50, null=True, blank=True)
    product_name_b = models.CharField(max_length=255, null=True, blank=True)
    company_b = models.CharField(max_length=255, null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'contraindicated_drug'
