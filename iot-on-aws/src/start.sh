#!/bin/bash

aws iot describe-endpoint > /tmp/iotendpoint.json
iot_endpoint=$(jq -r ".endpointAddress" /tmp/iotendpoint.json)
echo "Running sample application..."
python3 main.py \
        --endpoint $iot_endpoint \
        --cert keys/device-certificate.pem.crt \
        --key keys/device-private.pem.key \
        --client_id basicPubSub \
        --topic truck/freezer \
        --count 0
