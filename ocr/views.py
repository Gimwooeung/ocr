from django.shortcuts import render
import cv2
import easyocr
import numpy as np
import base64
import re
from .models import DrugName
# from main import PororoOcr
import easyocr
# from pororo.pororo import Pororo


import difflib
from difflib import get_close_matches
from difflib import SequenceMatcher
# import qweqweqw
# from main import PororoOcr
# from qweqweqw import Pororo

def preprocess_image(img):
    # 이미지 크기 조절
    img = cv2.resize(img, (0, 0), fx=1.5, fy=1.5)

    # 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 이진화
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 노이즈 제거 (가우시안 블러)
    img = cv2.GaussianBlur(binary, (5, 5), 0)

    # 글자 외곽선 강화
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, kernel)
    return img


def splits(list):
    list=list.split('(')[0]
    list=list.split('[')[0]
    return list
        # 수정된 결과를 리스트에 추가

matches = []

def process_image(image):
    # 이미지 파일 로드
    uploaded_image_data = image.read()
    image.seek(0)  # 파일 커서를 이미지 파일의 시작점으로 이동

    # easy OCR 엔진 초기화
    reader = easyocr.Reader(['ko', 'en'], gpu=True)

    # Pororo OCR 초기화
    # recognizer = Pororo(task="ocr", lang="ko")

    # 이미지를 RGB 색상 모드로 변환
    img_array = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    preprocess_image(img)
    # 이미지에 바운딩 박스와 텍스트 추가
    result = []

    for bbox, text, _ in reader.readtext(img):
        pt1 = tuple(map(int, bbox[0]))
        pt2 = tuple(map(int, bbox[2]))
        img_array = cv2.rectangle(img_array, pt1, pt2, color=(0, 255, 0), thickness=2)
        #result.append(re.sub(r'[^\w가-힣.]+', '', text))
        #result.append(text.split("(" or "[")[0])
        result.append(splits(text))

# 글자 전처리
    # result = re.sub(r'\(.*\)', '', result)
    # result = re.sub(r'\[.*\]', '', result)
    # result = [t.replace('본)', '') for t in result]
    # result = [t.replace('비)', '') for t in result]
    # result = [t.replace('`', '') for t in result]
    # result = [t.replace('~', '') for t in result]
    # result = [t.replace('!', '') for t in result]
    # result = [t.replace('@', '') for t in result]
    # result = [t.replace('#', '') for t in result]
    # result = [t.replace('$', '') for t in result]
    # #    r = [t.replace('%', '') for t in r]
    # result = [t.replace('^', '') for t in result]
    # result = [t.replace('&', '') for t in result]
    # result = [t.replace('*', '') for t in result]
    # result = [t.replace('(', '') for t in result]
    # result = [t.replace(')', '') for t in result]
    # result = [t.replace('-', '') for t in result]
    # result = [t.replace('_', '') for t in result]
    # result = [t.replace('=', '') for t in result]
    # result = [t.replace('+', '') for t in result]
    # result = [t.replace('[', '') for t in result]
    # result = [t.replace('{', '') for t in result]
    # result = [t.replace(']', '') for t in result]
    # result = [t.replace('}', '') for t in result]
    # result = [t.replace(';', '') for t in result]
    # result = [t.replace(':', '') for t in result]
    # result = [t.replace('"', '') for t in result]
    # result = [t.replace("'", '') for t in result]
    # result = [t.replace(',', '') for t in result]
    # result = [t.replace('<', '') for t in result]
    # result = [t.replace('.', '') for t in result]
    # result = [t.replace('>', '') for t in result]
    # result = [t.replace(' ', '') for t in result]

    # 결과 이미지와 인식 결과 반환
    result_img_data = cv2.imencode('.jpg', cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))[1].tobytes()
    uploaded_image_data = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
    uploaded_image_data = cv2.cvtColor(uploaded_image_data, cv2.COLOR_BGR2RGB)
    uploaded_image_data = cv2.imencode('.jpg', uploaded_image_data)[1].tobytes()
    # print("ocr에서 추출해온 값:",result)


    # 추가된 부분: 데이터베이스에서 약 이름 불러오기
    drug_names = [drug.drug_name for drug in DrugName.objects.all()]
    # print(drug_names)
    # 추가된 부분: OCR 결과와 데이터베이스의 약 이름 비교하기
    matched_drugs = []
    for p in range(len(result)):
        n = 1
        cutoff = 0.7
        k = result[p]
        matches_j = get_close_matches(k, drug_names, n, cutoff)
        if matches_j:
            matched_drugs.extend(matches_j)
    matched_drugs = list(set(matched_drugs)) # 중복제거
    # print("데이터베이스랑 메칭된 약: ",matched_drugs)
    # 추가된 부분: 일치하는 약 이름 반환하기
    return result_img_data, uploaded_image_data, matched_drugs, result
    return result_img_data, uploaded_image_data, result






def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']

        # 이미지 처리 및 OCR 수행
        result_img_data, uploaded_image_data, matched_drugs,result = process_image(image)
        # result_img_data, uploaded_image_data, result = process_image(image)

        # 결과값을 렌더링할 때 사용할 context 변수 생성
        context = {
            'uploaded_image_data': base64.b64encode(uploaded_image_data).decode('utf-8'),
            'result_img_data': base64.b64encode(result_img_data).decode('utf-8'),
            'result_data': result,
            'matched_drugs': matched_drugs,
            'matched_drugs': matched_drugs,
        }

        # 결과 이미지 반환
        return render(request, 'result.html', context)

    return render(request, 'index.html')
