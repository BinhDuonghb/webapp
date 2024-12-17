# Sử dụng Python image chính thức
FROM python:3.10-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file yêu cầu (requirements.txt) và cài đặt các dependency
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Expose port 5000 để Flask app chạy
EXPOSE 5000

# Chạy Flask application
CMD ["python", "app.py"]
