FROM node:20.9-alpine AS builder


WORKDIR /diploma-frontend

COPY ./diploma-frontend/package.json ./
COPY ./diploma-frontend/package-lock.json ./

RUN npm install --force

COPY ./diploma-frontend/ ./

RUN npm run build --prod


FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY --from=builder /diploma-frontend/dist/diploma-frontend /usr/share/nginx/html