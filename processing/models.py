import uuid
from django.db import models

class ProcessingRequest(models.Model):
    request_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

def upload_to(instance, filename):
    return f'processed_images/{instance.product_name}/{filename}'

class ProductImage(models.Model):
    request = models.ForeignKey(ProcessingRequest, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    input_image_url = models.URLField()
    output_image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
