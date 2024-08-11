FROM python:3.10.14-bookworm AS build_base

LABEL authors="Zoe Tsekas"
RUN echo "building base"


FROM build_base AS data_environment

RUN echo "building data environment"
RUN echo python3.10 --version


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

FROM data_environment AS data_code

RUN echo "building tank royal code"

WORKDIR /app/robocode

COPY ./robocode /app/robocode
COPY ./bots /app/bots

EXPOSE 7654

ENV DISPLAY=$DISPLAY

CMD ["java", "-jar", "robocode-tankroyale-server-0.24.1.jar", "--games=classic,melee", \
     "--port=7654", "--controller-secrets=Jwxwdd5V1QN1ySWIpv0UsQ", "--bot-secrets=wNzRU2AEwjsL1PFaZiM7lg"]