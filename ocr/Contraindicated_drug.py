import django.http
from ocr.models import ContraindicatedDrug
from django.db.models import Q
import itertools
import operator
from functools import reduce
import time

def drugContraindicated(drug):
    response = []
    drug_combinations = list(itertools.combinations(drug, 2))

    start_time = time.time()  # 메서드 실행 전 시간 측정
    contraindicated_drugs = ContraindicatedDrug.objects.filter(
        Q(
            reduce(operator.or_,
                   [Q(product_name_a__startswith=a, product_name_b__startswith=b) for a, b in drug_combinations]) |
            reduce(operator.or_,
                   [Q(product_name_a__startswith=b, product_name_b__startswith=a) for a, b in drug_combinations])
        )
    )
    for drug_pair in contraindicated_drugs:
        response.append(f"{drug_pair.product_name_a}와 {drug_pair.product_name_b}는(은) 병용금기약물입니다. 담당의사와 상의하세요.")



    end_time = time.time()  # 메서드 실행 후 시간 측정
    execution_time = end_time - start_time  # 실행 시간 계산

    print(f"메서드 실행 시간: {execution_time}초")

    return response
