# See https://sourcery.ai/blog/python-docker/ or https://jonathanmeier.io/using-pipenv-with-docker/ for an example
FROM python:3

ENV ENVIRONMENT Emulator

RUN pip install pipenv
#COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
#RUN pipenv install --system --deploy

