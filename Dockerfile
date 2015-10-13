FROM frolvlad/alpine-python3:latest

WORKDIR /src

COPY . /src/

RUN pip3 install .

ENTRYPOINT ["./wrapper"]
