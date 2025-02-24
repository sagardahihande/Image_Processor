import csv
import uuid
from io import StringIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import ProcessingRequest, ProductImage
from .tasks import process_images

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'Invalid file format'}, status=400)

        processing_request = ProcessingRequest.objects.create()
        decoded_file = csv_file.read().decode('utf-8')
        reader = csv.reader(StringIO(decoded_file))
        next(reader)

        for row in reader:
            product_name = row[1]
            image_urls = row[2].split(',')
            for url in image_urls:
                ProductImage.objects.create(
                    request=processing_request,
                    product_name=product_name,
                    input_image_url=url.strip()
                )

        process_images.delay(str(processing_request.request_id))
        return JsonResponse({'request_id': str(processing_request.request_id)})

@csrf_exempt
def check_status(request, request_id):
    processing_request = get_object_or_404(ProcessingRequest, request_id=request_id)
    return JsonResponse({'request_id': request_id, 'status': processing_request.status})
