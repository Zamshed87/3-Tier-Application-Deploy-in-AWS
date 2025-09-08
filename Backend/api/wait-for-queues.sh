#!/bin/bash
set -e

QUEUE_URL=${SQS_QUEUE_URL}

echo "Waiting for ElasticMQ queue $QUEUE_URL ..."

while true; do
    STATUS=$(aws --endpoint-url http://elasticmq:9324 sqs get-queue-attributes \
        --queue-url $QUEUE_URL \
        --attribute-names All 2>&1 || echo "error")

    if [[ "$STATUS" != *"error"* ]]; then
        echo "ElasticMQ queue ready."
        break
    fi

    echo "Waiting for ElasticMQ..."
    sleep 2
done

exec "$@"
