#!/usr/bin/env bash

docker run -it --rm \
  -p 80:80 \
  -v "$(pwd -P)/_dist/html":/var/www/html \
  --name 'php-dev-server' \
  'php:8.3.2-apache'