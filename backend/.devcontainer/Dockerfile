FROM python:3.12.2-bookworm

WORKDIR /workspace

# * install needed libs
COPY requirements/ requirements/
RUN pip install --upgrade pip
RUN pip3 install -r requirements/dev.txt
