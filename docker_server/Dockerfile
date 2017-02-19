FROM python:2.7
MAINTAINER Pradeep Kumar "ppradeepkumards@gmail.com"
COPY . /minion_server
WORKDIR /minion_server
RUN pip install -r dependency.txt
EXPOSE 22
EXPOSE 80
EXPOSE 443
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["minion_server_app.py"]
