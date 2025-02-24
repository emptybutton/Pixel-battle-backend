FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /certbot
COPY deployments/prod/certbot .

RUN uv pip install --system certbot certbot-nginx
ENV SSL_PATH=/mnt/ssl

HEALTHCHECK \
--start-period=1m \
--start-interval=0.5s \
--interval=1m \
CMD [[ -e ${SSL_PATH}/cert && -e ${SSL_PATH}/key ]]

CMD ["ash", "start-ssl-refresh.sh"]
