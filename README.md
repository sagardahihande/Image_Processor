# 🖼 Django Asynchronous Image Processor

This project is a Django-based system that processes images asynchronously from a CSV file. It:
- Accepts a CSV file with **Product Name** and **Image URLs**.
- Compresses images to **50% quality** asynchronously using **Celery & Redis**.
- Stores the processed images and tracks **processing status**.
- Provides a **Webhook** to notify when all images are processed.

## 🚀 Features
👉 **Django REST Framework** for API handling  
👉 **Asynchronous Image Processing** using Celery & Redis  
👉 **Webhook Support** to notify when processing completes  
👉 **Docker Support** for running Redis easily  
👉 **Postman Collection** for easy API testing  

## 📌 Tech Stack
- **Backend:** Django, Django REST Framework  
- **Async Tasks:** Celery  
- **Queue Broker:** Redis  
- **Database:** PostgreSQL / SQLite (default)  
- **Image Processing:** Pillow  

## 🛠 Installation Guide

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/image-processor.git
cd image-processor
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Database
```sh
python manage.py makemigrations processing
python manage.py migrate
```

### 5️⃣ Start Redis Server
**(Choose One)**  
If using **Docker**:
```sh
docker run -d --name redis-server -p 6379:6379 redis
```
If using **Windows Redis**:
```sh
redis-server
```

### 6️⃣ Start Celery Worker
```sh
celery -A image_processor worker --loglevel=info --pool=solo
```

### 7️⃣ Run Django Server
```sh
python manage.py runserver
```

## 🔥 API Endpoints & Usage

### 📌 Upload CSV File
**Endpoint:**  
```
POST /api/upload/
```
**Headers:**
```json
{
    "Content-Type": "multipart/form-data"
}
```
**Body:**  
- `file`: Upload your **CSV file** with product names and image URLs.

**Example Response:**
```json
{
    "request_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### 📌 Check Processing Status
**Endpoint:**  
```
GET /api/status/<request_id>/
```
**Example Response (Pending):**
```json
{
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "pending"
}
```
**Example Response (Completed):**
```json
{
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "completed"
}
```

### 📌 Webhook (Bonus Feature)
After processing is complete, the system sends a **POST request** to:
```
YOUR_WEBHOOK_URL
```
**Example Webhook Payload:**
```json
{
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "completed"
}
```

## ⚠️ Troubleshooting

| Issue | Solution |
|--------|----------|
| Postman returns `500 Internal Server Error` | Check Django logs: `python manage.py runserver` |
| Redis is not working | Restart Redis (`docker start redis-server` OR `redis-server`) |
| Celery task is not running | Make sure Celery is started: `celery -A image_processor worker --loglevel=info --pool=solo` |

## 📚 Future Improvements
- ✅ **Store processed images in AWS S3 or Cloud Storage**  
- ✅ **Add User Authentication & JWT Token Support**  
- ✅ **Improve Webhook Customization**  

## 🤝 Contributing
1. Fork the repo  
2. Create a new branch  
3. Make changes & test  
4. Submit a Pull Request  

## 📚 License
This project is licensed under the **MIT License**.

---
🚀 **Built with ❤️ by Sagar Dahihande **

