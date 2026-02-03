FROM php:8.2-fpm-alpine

# Install system dependencies
RUN apk add --no-cache     git     curl     libpng-dev     libzip-dev     zip     unzip     nginx     supervisor     icu-dev

# Install PHP extensions
RUN docker-php-ext-install pdo pdo_mysql zip gd exif intl

# Install Redis extension
RUN apk add --no-cache $PHPIZE_DEPS     && pecl install redis     && docker-php-ext-enable redis

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www/html

# Copy application files
COPY . .

# Set permissions
RUN mkdir -p /var/www/html/storage/framework/views \
    /var/www/html/storage/framework/cache \
    /var/www/html/storage/framework/sessions \
    /var/www/html/storage/logs \
    /var/www/html/bootstrap/cache
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

# Install dependencies (if composer.json exists)
RUN if [ -f composer.json ]; then composer install --no-interaction --optimize-autoloader --no-dev; fi

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Copy supervisor configuration
RUN echo "[supervisord]" > /etc/supervisord.conf &&     echo "nodaemon=true" >> /etc/supervisord.conf &&     echo "" >> /etc/supervisord.conf &&     echo "[program:php-fpm]" >> /etc/supervisord.conf &&     echo "command=php-fpm" >> /etc/supervisord.conf &&     echo "autostart=true" >> /etc/supervisord.conf &&     echo "autorestart=true" >> /etc/supervisord.conf &&     echo "" >> /etc/supervisord.conf &&     echo "[program:nginx]" >> /etc/supervisord.conf &&     echo "command=nginx -g 'daemon off;'" >> /etc/supervisord.conf &&     echo "autostart=true" >> /etc/supervisord.conf &&     echo "autorestart=true" >> /etc/supervisord.conf

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
