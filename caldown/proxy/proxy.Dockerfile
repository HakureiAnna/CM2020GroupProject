FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY ./proxy/nginx.conf /etc/nginx/conf.d/
