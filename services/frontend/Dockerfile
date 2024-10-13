FROM node:18-alpine AS build

WORKDIR /app

COPY services/frontend/package*.json ./

RUN npm install

COPY services/frontend/src/ ./src/

COPY services/frontend/public/ ./public/

ADD --chmod=777 https://upload.wikimedia.org/wikipedia/commons/7/75/Vinyl_record.svg ./public/vinyl_record.svg

RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]