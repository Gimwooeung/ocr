from django.shortcuts import render
import base64
from .models import DrugName,ContraindicatedDrug
from ocr.text_preprocessing import TextProcessor
from ocr.Contraindicated_drug import drugContraindicated
from ocr.Imageprocess import ImageProcessor
processor = TextProcessor() # 글자유사도 클래스 불러오기
image_processor = ImageProcessor() # OCR실행

def upload_image(request):
    if request.method == 'POST' and 'image1' in request.FILES and 'image2' in request.FILES:
        image1= request.FILES['image1']
        image2 = request.FILES['image2']
        # 이미지 파일 처리 로직 추가
        # image1_file과 image2_file을 사용하여 원하는 작업을 수행합니다.

        # 이미지 처리 및 OCR 수행
        result_img_data, uploaded_image_data, ocr, matched_drugs  = image_processor.process_image(image1)
        result_img_data2, uploaded_image_data2, ocr2, matched_drugs2 = image_processor.process_image2(image2)
        drugs=matched_drugs+matched_drugs2
        response = drugContraindicated(drugs)


        context = {
            # 'uploaded_image_data': base64.b64encode(uploaded_image_data).decode('utf-8'),
            # 'uploaded_image_data2': base64.b64encode(uploaded_image_data2).decode('utf-8'),
            'result_img_data': base64.b64encode(result_img_data).decode('utf-8'),
            'result_img_data2': base64.b64encode(result_img_data2).decode('utf-8'),
            #'result_data': ocr,
            #'result_data2': ocr2,
            'matched_drugs': drugs,
            'response':response
        }

        # 결과 이미지 반환
        return render(request, 'result.html', context)
        # return render(request, 'Contarindicated.html', context)

    return render(request, 'index.html')