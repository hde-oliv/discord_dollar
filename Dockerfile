FROM archlinux:latest

WORKDIR /tmp

RUN pacman -Syy firefox python python-pip geckodriver --noconfirm

WORKDIR /app

RUN pip install 'poetry==1.2.2'.

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider https://google.com || exit 1

CMD ["python", "discord_dollar/main.py"]
