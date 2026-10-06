FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY the test script into the container
COPY test_app.py .
COPY app.py .

# RUN the tests during the build phase. If tests fail, Docker stops building!
RUN pytest test_app.py

EXPOSE 5000
CMD ["python", "app.py"]