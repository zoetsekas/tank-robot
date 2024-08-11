FROM python:3.10.14-bookworm AS build_base

LABEL authors="Zoe Tsekas"
RUN echo "building base"


FROM build_base AS data_environment

RUN echo "building data environment"
RUN echo python3.10 --version

#RUN add-apt-repository ppa:graphics-drivers/ppa
#RUN apt-get update
#RUN apt-get install nvidia-driver-530


RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

RUN apt-get update

RUN apt-get install -y nvidia-container-toolkit

RUN apt-get update

RUN apt-get install xorg -y

#RUN apt-get update & apt-get install xserver-xorg-video-nvidia-530 xserver-xorg-core xinit -y

RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y ant && \
    apt-get clean;

RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

RUN apt-get install -y iputils-ping

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME


RUN pip install --no-cache-dir --upgrade pip

RUN pip install python-dotenv
RUN pip install "ray[all]"==2.34.0
RUN pip install gymnasium
RUN pip install jsonschema
RUN pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cu118
RUN pip install gputil
RUN pip install websocket-client
RUN pip install rel
RUN pip install colorama
RUN pip install PyYAML
RUN pip install torchrl

FROM data_environment AS data_code

RUN echo "building tank royal code"

WORKDIR /app

COPY ./rl /app/rl
COPY ./robocode /app/robocode
COPY ./bots /app/bots
COPY ./system.env /app/.env

ENV PYTHONPATH=/app

ENTRYPOINT [ "python", "./rl/main.py"]

#CMD [ "--action=train"]