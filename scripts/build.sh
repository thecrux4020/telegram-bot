#!/bin/sh

rm -rf ./scripts/build
pip install --target ./scripts/package -r requirements.txt
mkdir ./scripts/build
zip -r ./scripts/build/deploy.zip app/ main.py ./scripts/package/
rm -rf ./scripts/package