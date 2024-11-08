FROM python:3.12-slim as fastapi-server

WORKDIR /var/www

RUN apt-get update && apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

ENV LC_ALL="en_US.UTF-8"
ENV LC_CTYPE="en_US.UTF-8"

COPY --chown=www-data:www-data . /var/www/

#### Install al packages and modules
RUN pip3 install -r requirements.txt

CMD alembic upgrade head && fastapi run --workers 4 main.py
