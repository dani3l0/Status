FROM python:3.11-alpine
WORKDIR /app

# install requirements in seperate layer to benefit from caching
COPY ./requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

# copy only necessary things
COPY ./html ./html
COPY ./lib ./lib
COPY ./status.py .

ENV STATUS_CUSTOM_ROOT_PATH=/host_root
CMD ["python", "status.py", "--no-config"]
EXPOSE 9090
