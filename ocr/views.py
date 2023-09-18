from django.shortcuts import render
import base64
from ocr.Contraindicated_drug import drugContraindicated
from ocr.Imageprocess import ImageProcessor
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

image_processor = ImageProcessor() # OCR실행
def chat_view(request):
    return render(request, 'chat.html')
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and 'image1' in request.FILES and 'image2' in request.FILES:
        image1= request.FILES['image1']
        image2 = request.FILES['image2']

        # 이미지 처리 및 OCR 수행
        result_img_data, uploaded_image_data, ocr, matched_drugs  = image_processor.process_image(image1)
        result_img_data2, uploaded_image_data2, ocr2, matched_drugs2 = image_processor.process_image(image2)
        drugs=matched_drugs+matched_drugs2
        response = drugContraindicated(drugs)

        context = {
            'result_img_data': base64.b64encode(result_img_data).decode('utf-8'),
            'result_img_data2': base64.b64encode(result_img_data2).decode('utf-8'),
            'matched_drugs': drugs,
            'response':response
        }

        # 결과 이미지 반환
        return render(request, 'result.html', context)

    return render(request, 'index.html')

@csrf_exempt
def upload_image_chat_api(request):
    if request.method == 'POST' and 'image1' in request.FILES and 'image2' in request.FILES:
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']

        # 이미지 처리 및 OCR 수행
        result_img_data, uploaded_image_data, ocr, matched_drugs  = image_processor.process_image(image1)
        result_img_data2, uploaded_image_data2, ocr2, matched_drugs2 = image_processor.process_image(image2)
        drugs = matched_drugs + matched_drugs2
        response = drugContraindicated(drugs)

        context = {
            'result_img_data': base64.b64encode(result_img_data).decode('utf-8'),
            'result_img_data2': base64.b64encode(result_img_data2).decode('utf-8'),
            'matched_drugs': drugs,
            'response': response
        }

        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'Invalid request method or missing files.'})