import django.http
from ocr.models import ContraindicatedDrug
from django.db.models import Q

response=[]

def drugContraindicated(drug):
    print(drug)
    for i in range(len(drug)) :
        for j in range(len(drug)) :
            contraindicated_drugs = ContraindicatedDrug.objects.filter(
                Q(product_name_a__icontains=drug[i], product_name_b__icontains=drug[j])|Q(product_name_b__icontains=drug[i], product_name_a__icontains=drug[j]))
            print("병용금기 약물 매칭중", contraindicated_drugs)
            if contraindicated_drugs:
                for drug_pair in contraindicated_drugs:
                    response.append(f"{drug_pair.product_name_a}와 {drug_pair.product_name_b}는(은) 범용금기약물입니다. 담당의사와 상의하세요.")
    return response