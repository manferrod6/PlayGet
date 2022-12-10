FROM python:3.11.0-alpine3.17

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

RUN  apk update \
	&& apk add --no-cache python3-dev \
	&& pip install pillow \
	&& pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py","runserver", "0.0.0.0:8000"]