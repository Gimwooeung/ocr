import time
import cv2
import numpy as np
import easyocr
from ocr.pororo.pororo import Pororo
from difflib import get_close_matches
from .models import DrugName, ContraindicatedDrug  # Django 모델 가져오기
from . import text_preprocessing

# 추가된 부분: 데이터베이스에서 약 이름 불러오기
drug_names = [drug.drug_name for drug in DrugName.objects.all()]

class ImageProcessor:
    def __init__(self):
        self.reader = easyocr.Reader(['ko', 'en'], gpu=True) # OCR 감지
        self.recognizer = Pororo(task="ocr", lang="ko") # OCR 인식
        self.text_processor = text_preprocessing.TextProcessor() # 텍스트 전처리

    def process_image(self, image):
        start_time = time.time()  # 시작 시간 측정
        uploaded_image_data = image.read()
        image.seek(0)

        # 이미지 디코딩
        img_array = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        # EasyOCR을 사용하여 텍스트 감지
        result = self.reader.readtext(img)

        # 텍스트와 인식 결과를 저장할 목록 초기화
        tt = []

        for box in result:
            # EasyOCR 결과에서 텍스트와 좌표 추출
            text = box[1]
            x_min, y_min = box[0][0]
            x_max, y_max = box[0][2]

            # 감지된 텍스트 주변에 사각형 그리기
            cv2.rectangle(img_array, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

            # 감지된 텍스트 주변의 이미지 자르고 Pororo OCR을 사용하여 인식
            cropped_img = img[int(y_min):int(y_max), int(x_min):int(x_max)]
            recognition_result = self.recognizer(cropped_img)

            # 텍스트와 인식 결과를 목록에 저장
            tt.append((text, recognition_result))

        # 텍스트 감지 결과 시각화
        result_img_data = cv2.imencode('.jpg', cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))[1].tobytes()
        uploaded_image_data = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        uploaded_image_data = cv2.cvtColor(uploaded_image_data, cv2.COLOR_BGR2RGB)
        uploaded_image_data = cv2.imencode('.jpg', uploaded_image_data)[1].tobytes()

        # 텍스트 전처리 및 약물 이름과 매치
        recognized_results = [recognition_result for text, recognition_result in tt]
        recognized_results_flat = [result for sublist in recognized_results for result in sublist]
        pre = recognized_results_flat
        ocr = self.text_processor.process_ocr(pre)

        matched_drugs = []

        for p in range(len(ocr)):
            n = 1
            cutoff = 0.7
            k = ocr[p]

            # 비슷한 단어를 'mg'로 대체
            if '밀리그람' in k or '밀리그램' in k or '일리그람' in k or '일리그램' in k:
                k = k.replace('밀리그람', 'mg')
                k = k.replace('밀리그램', 'mg')
                k = k.replace('일리그람', 'mg')
                k = k.replace('일리그램', 'mg')

            # 약물 이름과 유사한 항목 찾기
            matches_j = get_close_matches(k, drug_names, n, cutoff)

            if matches_j:
                matched_drugs.extend(matches_j)

        matched_drugs = list(set(matched_drugs))

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"실행 시간: {execution_time} 초")
        return result_img_data, uploaded_image_data, ocr, matched_drugs
