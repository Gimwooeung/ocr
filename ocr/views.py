from django.shortcuts import render
import cv2
import numpy as np
import base64
from .models import DrugName,ContraindicatedDrug
import easyocr
from difflib import get_close_matches
from ocr.pororo.pororo import Pororo
from ocr.text_preprocessing import TextProcessor
from ocr.Contraindicated_drug import drugContraindicated

processor = TextProcessor() # 글자유사도 클래스 불러오기

# 리스트 변수 생성
matches = []
recognized_text = []
values = []

# 추가된 부분: 데이터베이스에서 약 이름 불러오기
drug_names = [drug.drug_name for drug in DrugName.objects.all()]
durg_a = [drug.product_name_a for drug in ContraindicatedDrug.objects.all()]
durg_b = [drug.product_name_b for drug in ContraindicatedDrug.objects.all()]
contra = [drug.details for drug in ContraindicatedDrug.objects.all()]

def process_image(image):
    # 이미지 파일 로드
    uploaded_image_data = image.read()
    image.seek(0)  # 파일 커서를 이미지 파일의 시작점으로 이동

    # easy OCR 엔진 초기화
    reader = easyocr.Reader(['ko', 'en'], gpu=True)

    # Pororo OCR 엔진 초기화
    recognizer = Pororo(task="ocr", lang="ko")

    # 이미지를 RGB 색상 모드로 변환
    img_array = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

    # EasyOCR을 이용하여 문자 검출 수행
    result = reader.readtext(img)

    # 이미지에 바운딩 박스와 텍스트 추가
    tt = []
    for box in result :
        text = box[1]
        x_min, y_min = box[0][0]
        x_max, y_max = box[0][2]
        cropped_img = img[int(y_min):int(y_max), int(x_min):int(x_max)]
        cv2.rectangle(img_array, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
        recognition_result = recognizer(cropped_img)
        tt.append((text,recognition_result))

    # 결과 이미지와 인식 결과 반환
    result_img_data = cv2.imencode('.jpg', cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))[1].tobytes()
    uploaded_image_data = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
    uploaded_image_data = cv2.cvtColor(uploaded_image_data, cv2.COLOR_BGR2RGB)
    uploaded_image_data = cv2.imencode('.jpg', uploaded_image_data)[1].tobytes()

    # 인식결과를 리스트에 담는과정
    recognized_results = [recognition_result for text, recognition_result in tt]
    recognized_results_flat = [result for sublist in recognized_results for result in sublist]
    pre = recognized_results_flat
    ocr = processor.process_ocr(pre)

    # 글자유사도
    matched_drugs = []
    for p in range(len(ocr)):
        n = 1
        cutoff = 0.7
        k = ocr[p]
        if '밀리그람' or '밀리그램' or '일리그람' or '일리그램' in k:
            k = k.replace('밀리그람', 'mg')
            k = k.replace('밀리그램', 'mg')
            k = k.replace('일리그람', 'mg')
            k = k.replace('일리그램', 'mg')
        matches_j = get_close_matches(k, drug_names, n, cutoff)
        if matches_j:
            matched_drugs.extend(matches_j)
    matched_drugs = list(set(matched_drugs)) # 중복제거
    return result_img_data, uploaded_image_data, ocr, matched_drugs

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']

        # 이미지 처리 및 OCR 수행
        result_img_data, uploaded_image_data, ocr, matched_drugs  = process_image(image)
        # result_img_data, uploaded_image_data, result = process_image(image)

        responses = drugContraindicated(matched_drugs)
        response = set(responses)
        print("야이가아",response)

        context = {
            'uploaded_image_data': base64.b64encode(uploaded_image_data).decode('utf-8'),
            'result_img_data': base64.b64encode(result_img_data).decode('utf-8'),
            'result_data': ocr,
            'matched_drugs': matched_drugs,
            'response':response
        }

        # 결과 이미지 반환
        return render(request, 'result.html', context)

    return render(request, 'index.html')