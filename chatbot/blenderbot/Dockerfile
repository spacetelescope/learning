FROM python:3.8

RUN apt update
RUN apt install -y libblas-dev liblapack-dev gfortran

RUN git clone https://github.com/facebookresearch/ParlAI.git /opt/ParlAI

WORKDIR /opt/ParlAI

RUN pip install -U pip setuptools wheel

RUN pip install torch fairseq  # if killed increase ram to build pytorch

RUN pip install -r requirements.txt

RUN python3 setup.py develop

CMD ["parlai", "interactive_web", "--host", "0.0.0.0", "--task", "blended_skill_talk:all", "-mf", "zoo:blenderbot2/blenderbot2_400M/model", "--search-server", "http://chatbot-server:5000"]
