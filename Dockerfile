FROM python:3.12-alpine

COPY ./pyproject.toml .

# Update repositories and upgrade packages
RUN sed -i -e 's/v3\.18/edge/g' /etc/apk/repositories \
    && apk upgrade --update-cache --available  \
    && apk add --no-cache gcc g++ libxslt-dev librdkafka-dev \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install pip-tools \
    && python3 -m piptools compile --extra producer -o requirements.txt pyproject.toml \
    && pip3 install -r requirements.txt --no-cache-dir 

WORKDIR /app

COPY /adapter /app/adapter


# Set permissions for files copied into the image
RUN chmod +r /app/adapter/generic_file_adapter.py

RUN adduser -D -g '' worker
USER worker

CMD [ "python3", "-m", "adapter.generic_file_adapter" ]
