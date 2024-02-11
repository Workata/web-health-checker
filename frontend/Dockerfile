# * BUILD STAGE
FROM node:21-alpine3.18 as builder

WORKDIR /app
COPY package*.json ./

RUN npm install --force
COPY . .
RUN npm run build

# * UP NGINX STAGE
FROM nginx:1.25.3-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80
