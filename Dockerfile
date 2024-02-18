FROM ghcr.io/merklebot/hackathon-arm-image:master as build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH

ARG Version
ARG GitCommit
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" 


COPY requirements.txt requirements.txt
RUN apt-get install -y portaudio19
RUN apt-get install -y python3-pyaudio
RUN apt-get install -y flac
RUN python3.8 -m pip install -r requirements.txt
COPY . .

CMD ["python3.8", "main.py"]
