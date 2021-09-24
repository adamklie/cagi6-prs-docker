FROM ubuntu:latest  
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y python3.6 python3-pip python3-setuptools python3-dev libcurl4-gnutls-dev libxml2-dev libssl-dev wget unzip
RUN pip3 install --upgrade pip

ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

ADD . .

# installing python libraries
RUN pip3 install --no-cache-dir -r python_requirements.txt

# installing plink
RUN wget https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20210606.zip
RUN unzip plink_linux_x86_64_20210606.zip

RUN chmod -R 777 /app/data/
RUN chmod -R 777 /app/output/

CMD ["bash", "/app/MGB_10_all.sh"]
