# --- Build stage ---
FROM node:20-alpine AS build
WORKDIR /app
# Use Taobao NPM mirror (huge speedup in China)
RUN npm config set registry https://registry.npmmirror.com

COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Serve stage ---
FROM nginx:1.27-alpine
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
