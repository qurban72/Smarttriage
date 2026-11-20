# Stage 1: build
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

# VITE_API_URL build ke waqt chahiye (compose / Railway ARG ke through pass hota hai)
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Stage 2: serve
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html

# Template mein sirf PORT substitute ho
ENV PORT=80
ENV NGINX_ENVSUBST_FILTER=^PORT$

EXPOSE 80
