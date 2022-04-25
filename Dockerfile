FROM python:3
ADD RandemonMain.py /
RUN pip install requirements.txt
CMD ["python",  "./RandemonMain.py"]