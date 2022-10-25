FROM python:3-slim
LABEL maintainer="Michael Pacheco <michael.dias@aluno.ufop.edu.br>"
COPY src/ /app/
COPY cert.pem/ /app/
COPY key.pem/ /app/
COPY requirements.txt /app/
WORKDIR /app/
RUN pip install --upgrade setuptools pip
RUN pip install -r requirements.txt
RUN echo "Running $(python --version)"
ENTRYPOINT ["python"]
CMD ["web_service.py"]
EXPOSE 5050