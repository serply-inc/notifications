#!/bin/bash
PHASE=$1
case "$PHASE" in
    pre)
            rm -r ./src/layer/python/
            mkdir -p ./src/layer/python/lib/python3.9/site-packages
            cp ./src/serply_*.py ./src/layer/python/lib/python3.9/site-packages
            pip3 install -r ./src/layer/requirements.txt -t ./src/layer/python/lib/python3.9/site-packages
            ;;
    post)   
            # do something
            ;;
    *)
            echo "Please provide a valid cdk_hooks phase"
            exit 64
esac