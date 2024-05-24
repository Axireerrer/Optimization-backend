FROM python:latest
WORKDIR /service
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY . /service
COPY requirements.txt /service/requirements.txt
EXPOSE 8000
RUN pip install -r /service/requirements.txt
