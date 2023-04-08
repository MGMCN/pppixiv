#!/bin/sh
echo "username=$1" >> .env
echo "password=$2" >> .env
python3 app.py