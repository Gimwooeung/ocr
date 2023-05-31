import time
import cv2
import numpy as np
import easyocr
from ocr.pororo.pororo import Pororo
from difflib import get_close_matches
from .models import DrugName,ContraindicatedDrug

# 추가된 부분: 데이터베이스에서 약 이름 불러오기
drug_names = [drug.drug_name for drug in DrugName.objects.all()]
durg_a = [drug.product_name_a for drug in ContraindicatedDrug.objects.all()]
durg_b = [drug.product_name_b for drug in ContraindicatedDrug.objects.all()]
contra = [drug.details for drug in ContraindicatedDrug.objects.all()]

class ImageProcessor:
    def __init__(self):
        self.reader = easyocr.Reader(['ko', 'en'], gpu=True)
        self.recognizer = Pororo(task="ocr", lang="ko")

    def process_image(self, image):
        start_time = time.time()  # Measure start time
        uploaded_image_data = image.read()
        image.seek(0)

        img_array = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        result = self.reader.readtext(img)

        tt = []
        for box in result:
            text = box[1]
            x_min, y_min = box[0][0]
            x_max, y_max = box[0][2]
            cropped_img = img[int(y_min):int(y_max), int(x_min):int(x_max)]
            cv2.rectangle(img_array, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            recognition_result = self.recognizer(cropped_img)
            tt.append((text, recognition_result))

        result_img_data = cv2.imencode('.jpg', cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))[1].tobytes()
        uploaded_image_data = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        uploaded_image_data = cv2.cvtColor(uploaded_image_data, cv2.COLOR_BGR2RGB)
        uploaded_image_data = cv2.imencode('.jpg', uploaded_image_data)[1].tobytes()

        recognized_results = [recognition_result for text, recognition_result in tt]
        recognized_results_flat = [result for sublist in recognized_results for result in sublist]
        pre = recognized_results_flat
        ocr = self.process_ocr(pre)

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
        matched_drugs = list(set(matched_drugs))

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Execution time: {execution_time} seconds")
        return result_img_data, uploaded_image_data, ocr, matched_drugs
    def process_image2(self, image):
        start_time = time.time()  # Measure start time
        uploaded_image_data = image.read()
        image.seek(0)

        img_array = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        result = self.reader.readtext(img)

        tt = []
        for box in result:
            text = box[1]
            x_min, y_min = box[0][0]
            x_max, y_max = box[0][2]
            cropped_img = img[int(y_min):int(y_max), int(x_min):int(x_max)]
            cv2.rectangle(img_array, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            recognition_result = self.recognizer(cropped_img)
            tt.append((text, recognition_result))

        result_img_data = cv2.imencode('.jpg', cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))[1].tobytes()
        uploaded_image_data = cv2.imdecode(np.frombuffer(uploaded_image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        uploaded_image_data = cv2.cvtColor(uploaded_image_data, cv2.COLOR_BGR2RGB)
        uploaded_image_data = cv2.imencode('.jpg', uploaded_image_data)[1].tobytes()

        recognized_results = [recognition_result for text, recognition_result in tt]
        recognized_results_flat = [result for sublist in recognized_results for result in sublist]
        pre = recognized_results_flat
        ocr = self.process_ocr(pre)

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
        matched_drugs = list(set(matched_drugs))

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Execution time: {execution_time} seconds")
        return result_img_data, uploaded_image_data, ocr, matched_drugs

    def process_ocr(self, ocr):
        # Process OCR logic
        # Replace with your implementation
        return ocr