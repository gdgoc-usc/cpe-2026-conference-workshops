#!/bin/bash

echo "Running sample application..."
python3 generic_example.py \
        --endpoint $iot_endpoint \
        --cert keys/rigney-certificate.pem.crt \
        --key keys/rigney-private.pem.key \
        --client_id basicPubSub \
        --topic rigney/temp \
        --count 0
