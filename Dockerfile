# grab the latest ubuntu base image
FROM ubuntu:latest

# set an environmental variable that I'm not sure about yet
ENV DEBIAN_FRONTEND=noninteractive

# install Python and pip
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y python3.6 python3-pip python3-setuptools python3-dev libcurl4-gnutls-dev libxml2-dev libssl-dev wget unzip
RUN pip3 install --upgrade pip

# set working dir
ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

# Add all the files locally to the Docker
ADD . .

# installing python libraries
RUN pip3 install --no-cache-dir -r python_requirements.txt

# installing plink
RUN wget https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20210606.zip
RUN unzip plink_linux_x86_64_20210606.zip

# making dirs readable and writeable
RUN chmod -R 777 /app/input/
RUN chmod -R 777 /app/output/

# run the script inside the docker
CMD ["bash", "/app/main_test.sh"]
