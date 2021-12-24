FROM python:3.8

RUN apt update
RUN apt install -y libblas-dev liblapack-dev gfortran

RUN git clone https://github.com/facebookresearch/ParlAI.git /opt/ParlAI

WORKDIR /opt/ParlAI

RUN pip install -U pip setuptools wheel

# if killed increase ram to build pytorch
RUN pip install torch fairseq slackclient transformers

RUN pip install -r requirements.txt

RUN python3 setup.py develop

CMD python $SCRIPT --host 0.0.0.0 --task $TASK -mf $MODEL --search-server http://chatbot-server:5000/search
