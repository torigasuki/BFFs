# python 3.11 버전 이미지를 사용해 빌드
FROM python:3.11

# .pyc 파일을 생성하지 않도록 설정합니다.
ENV PYTHONDONTWRITEBYTECODE 1

# 파이썬 로그가 버퍼링 없이 즉각적으로 출력하도록 설정합니다.
ENV PYTHONUNBUFFERED 1

# /app/ 디렉토리를 생성합니다.
RUN mkdir /app/

# /app/ 경로를 작업 디렉토리로 설정합니다.
WORKDIR /app/

# poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

# 호스트의 pyproject.toml 파일과 poetry.lock 파일을 컨테이너로 복사합니다.
COPY ./django/pyproject.toml ./django/poetry.lock ./

# 종속성 설치
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# gunicorn을 사용하기 위한 패키지를 설치합니다.
RUN pip install gunicorn psycopg2
