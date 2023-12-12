FROM nogil/python

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN chmod +x runAllDemos.sh

CMD ["./runAllDemos.sh"]