#!/bin/ash

rm -rf /etc/letsencrypt/live/certfolder*

certbot certonly \
    -n \
    --agree-tos \
    -m $DOMAIN_EMAIL \
    -d $DOMAIN \
    --key-type rsa \
    --webroot \
    -w /mnt/acme-challenge

ls -R -l /etc/letsencrypt/live/

cp /etc/letsencrypt/live/${DOMAIN}/fullchain.pem ${SSL_PATH}/cert.pem
cp /etc/letsencrypt/live/${DOMAIN}/privkey.pem ${SSL_PATH}/key.pem
