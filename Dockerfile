# syntax = docker/dockerfile:experimental
FROM latonaio/l4t:latest

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=direct-next-service \
    AION_HOME=/var/lib/aion

# Setup Directoties
RUN mkdir -p ${AION_HOME}/$POSITION/$SERVICE

WORKDIR ${AION_HOME}/$POSITION/$SERVICE

RUN apt-get update -y && apt-get install -y \
    v4l-utils \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


# Install dependencies
RUN pip3 install --upgrade pip

ADD . .
# RUN --mount=type=cache,target=/root/.cache/pip python3 setup.py install
RUN python3 setup.py install

CMD ["python3", "-m", "directnext"]


