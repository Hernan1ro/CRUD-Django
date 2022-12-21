FROM python:3.10

WORKDIR /proyect
COPY requirements.txt /proyect/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /proyect/requirements.txt

COPY . /proyect

CMD bash -c "while true; do sleep 1; done"