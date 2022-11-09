FROM python:3
LABEL maintainer="Michael Pacheco <michael.dias@aluno.ufop.edu.br>"
COPY src/ /app
COPY cert.pem/ /app
COPY key.pem/ /app
COPY requirements.txt /app
WORKDIR /app/
RUN pip install --upgrade setuptools pip
RUN pip install -r requirements.txt
RUN echo "Running $(python --version)"
ENTRYPOINT ["python"]
EXPOSE 5050
CMD ["web_service.py"]
