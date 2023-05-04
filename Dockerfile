FROM python:3.9
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple --trusted-host=pypi.douban.com

EXPOSE 80
CMD ["python", "app.py"]