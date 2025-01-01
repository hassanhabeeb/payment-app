# nginx/Dockerfile
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom configurations
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/
COPY includes/ /etc/nginx/includes/

# Create ssl directory
# RUN mkdir -p /etc/nginx/ssl

# Add SSL certificates if you have them
# COPY ssl/ /etc/nginx/ssl/

# Forward request logs to Docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]