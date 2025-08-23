FROM nginx:1.27-alpine3.21-perl

COPY deployments/prod/https-server/nginx.conf /etc/nginx/nginx.conf
COPY deployments/prod/https-server/backend.conf.template /etc/nginx/templates
