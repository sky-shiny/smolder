FROM mcameron/smolder:latest

WORKDIR /src

COPY . /src/

RUN pip3 install .

ENTRYPOINT ["./wrapper"]
