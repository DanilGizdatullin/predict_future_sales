FROM nielsborie/ml-docker

ENV PROJECT_PATH=/var/www/predict_future_sales/ \
    PIP_CACHE_DIR=/tmp/.cache/pip \
    PYTHONPATH=${PYTHONPATH}:${PROJECT_PATH}

WORKDIR ${PROJECT_PATH}

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
