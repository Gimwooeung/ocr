from django.db import models

# Create your models here.
class DrugName(models.Model):
    drug_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'drug_name'

class ContraindicatedDrug(models.Model):
    ingredienta = models.CharField(max_length=255)
    ingredient_codea = models.CharField(max_length=50)
    product_namea = models.CharField(max_length=255)
    companya = models.CharField(max_length=255)
    ingredientb = models.CharField(max_length=255, null=True, blank=True)
    ingredient_codeb = models.CharField(max_length=50, null=True, blank=True)
    product_nameb = models.CharField(max_length=255, null=True, blank=True)
    companyb = models.CharField(max_length=255, null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'contraindicated_drug'
