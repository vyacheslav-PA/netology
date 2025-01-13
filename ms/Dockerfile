FROM ubuntu:22.04
LABEL description="Build nginx"
VOLUME /var/log/nginx/
RUN apt update  && apt install nginx -y
COPY nginx.conf /etc/nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]