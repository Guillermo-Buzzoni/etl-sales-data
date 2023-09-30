FROM python:3.11.4

WORKDIR /app

RUN pip install pandas psycopg2

# Copia los archivos del directorio actual al contenedor en /app
COPY etl.py .
COPY sales_data.csv .

CMD ["python", "etl.py"]
