# Build Stage
FROM node:lts-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --omit-dev
RUN ls -la /app/dist

# Serve Stage
FROM nginx:alpine 

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/payment-app/browser /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]

