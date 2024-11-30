#base image
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Menambahkan langkah untuk memeriksa apakah uvicorn berhasil terinstal
RUN which uvicorn  # Memastikan uvicorn dapat ditemukan di PATH

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
