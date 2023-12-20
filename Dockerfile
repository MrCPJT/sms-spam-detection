FROM public.ecr.aws/lambda/python:3.10

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  POETRY_VERSION=1.7.1

# System deps:
RUN pip install "poetry==$POETRY_VERSION"


# COPY poetry.lock pyproject.toml /code/
COPY pyproject.toml .
COPY poetry.lock .

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# RUN python -c "import nltk; nltk.download('punkt')"
# RUN python -c "import nltk; nltk.download('wordnet')"
# RUN python -c "import nltk; nltk.download('stopwords')"

# # Project initialization:
# RUN poetry config virtualenvs.create false \
#   && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY model.bin .
COPY lambda_function.py .

CMD ["lambda_function.lambda_handler"]