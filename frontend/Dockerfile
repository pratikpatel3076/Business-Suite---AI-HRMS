FROM node:20-alpine AS build

LABEL org.opencontainers.image.title="Gemeinsam Web"
LABEL org.opencontainers.image.description="Gemeinsam frontend web app"

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# The app reads runtime config from public/app-config.js; this build arg only
# affects callers that rely on the Vite compile-time fallback.
ARG VITE_API_BASE_URL=/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

FROM nginx:1.27-alpine

LABEL org.opencontainers.image.title="Gemeinsam Web"
LABEL org.opencontainers.image.description="Gemeinsam frontend web app"

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
