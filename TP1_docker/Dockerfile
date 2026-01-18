FROM python:3.13
WORKDIR /app
RUN pip install flask pymongo
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
