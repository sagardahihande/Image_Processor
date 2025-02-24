import uuid
import requests
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from celery import shared_task
from .models import ProcessingRequest, ProductImage

@shared_task
def process_images(request_id):
    processing_request = ProcessingRequest.objects.get(request_id=request_id)
    images = ProductImage.objects.filter(request=processing_request)

    for image in images:
        response = requests.get(image.input_image_url, stream=True)
        if response.status_code == 200:
            img = Image.open(response.raw)
            output = BytesIO()
            img.save(output, format="JPEG", quality=50)
            output.seek(0)

            output_path = f'processed_images/{image.product_name}/{uuid.uuid4()}.jpg'
            default_storage.save(output_path, ContentFile(output.read()))

            image.output_image = output_path
            image.status = 'completed'
            image.save()

    processing_request.status = 'completed'
    processing_request.save()
    trigger_webhook(request_id)

def trigger_webhook(request_id):
    webhook_url = "YOUR_WEBHOOK_URL"
    requests.post(webhook_url, json={"request_id": str(request_id), "status": "completed"})
