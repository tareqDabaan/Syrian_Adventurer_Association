FROM python:3.11.4-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /adventurerweb

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "/adventurerweb/start.sh" ]

# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]