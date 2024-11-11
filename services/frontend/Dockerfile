FROM node:18-alpine AS build

WORKDIR /app

COPY services/frontend/package*.json ./

RUN npm install

COPY services/frontend/src/ ./src/

COPY services/frontend/public/ ./public/

ADD --chmod=777 https://upload.wikimedia.org/wikipedia/commons/7/75/Vinyl_record.svg ./public/vinyl_record.svg

RUN npm run build

FROM nginx:stable-alpine

RUN apk add --no-cache openssl

RUN mkdir -p /etc/ssl/private /etc/ssl/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/server.key \
    -out /etc/ssl/certs/server.crt \
    -subj "/C=PL/ST=Masovian/L=Warsaw/O=TuneCube/OU=IT/CN=tune_frontend"

RUN rm /etc/nginx/conf.d/default.conf

COPY services/frontend/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]