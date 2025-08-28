FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends gettext libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY --from=builder /app /app

COPY ./compose/local/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/local/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

ENV PATH=/root/.local/bin:$PATH

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8080

ENV PORT=8080

CMD [ "/start.sh" ]