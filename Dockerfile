ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev python3.6 python3-pip python3-setuptools python3-dev libcurl4-gnutls-dev libxml2-dev libssl-dev
RUN pip3 install --upgrade pip

ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

ADD . .

# installing python libraries
#RUN pip3 install -r python_requirements.txt

CMD ["bash", "/app/main.sh"]
