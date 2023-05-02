FROM python:3.11-alpine
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt
CMD ["python", "status.py", "--no-config"]
EXPOSE 9090
