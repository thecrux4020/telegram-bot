#!/bin/sh

rm -rf ./scripts/build
pip install --target ./scripts/package -r requirements.txt
mkdir ./scripts/build
zip -r ./scripts/build/deploy.zip app/ main.py settings.ini
cd ./scripts/package && zip -rg ../build/deploy.zip * && cd ../../
rm -rf ./scripts/package
