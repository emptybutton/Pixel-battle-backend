FROM redis:7.4.1-alpine3.20 AS redis-cluster-node

HEALTHCHECK \
--start-interval=0s \
--interval=1s \
--retries=30 \
CMD ash /mnt/scripts/is-node-ok.sh

ENTRYPOINT [""]
CMD ["ash", "/mnt/scripts/start-node.sh"]
