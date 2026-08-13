FROM php:5.6-apache

RUN sed -i \
    -e 's|deb.debian.org|archive.debian.org|g' \
    -e 's|security.debian.org|archive.debian.org|g' \
    /etc/apt/sources.list \
 && sed -i '/stretch-updates/d' /etc/apt/sources.list \
 && echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid

RUN apt-get update --allow-insecure-repositories \
 && apt-get install -y --allow-unauthenticated \
    libpng-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
 && docker-php-ext-configure gd \
      --with-freetype-dir=/usr/include/ \
      --with-jpeg-dir=/usr/include/ \
 && docker-php-ext-install gd mysql mysqli
 RUN echo '<Directory /var/www/html/admin>\n\
    AllowOverride All\n\
</Directory>' >> /etc/apache2/apache2.conf