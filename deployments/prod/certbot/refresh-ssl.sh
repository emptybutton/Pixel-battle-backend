#!/bin/ash

rm -rf /etc/letsencrypt/live/certfolder*

certbot certonly \
    -m $DOMAIN_EMAIL \
    -d $DOMAIN \
    --standalone \
    --cert-name=certfolder \
    --key-type rsa \
    --agree-tos

cp /etc/letsencrypt/live/certfolder*/fullchain.pem ${SSL_PATH}/cert.pem
cp /etc/letsencrypt/live/certfolder*/privkey.pem ${SSL_PATH}/key.pem
