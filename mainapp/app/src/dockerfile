FROM python:3.9.1
COPY . /src
WORKDIR /src
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt \
    && rm -rf /root/.cache/pip
