FROM archlinux:latest

WORKDIR /tmp

RUN pacman -Syy firefox python python-pip geckodriver --noconfirm

WORKDIR /app

RUN pip install 'poetry==1.2.2'.

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

CMD ["python", "discord_dollar/main.py"]
