FROM python:3.9

RUN pip install flask elasticsearch-dsl "elasticsearch>=7.0.0,<8.0.0"

WORKDIR /opt/chatbot-server
COPY server.py .

ENV FLASK_APP=server
CMD ["flask", "run", "-h", "0.0.0.0"]
