# ============================================================
# STAGE 1 — Build React application
# ============================================================

FROM node:22-alpine AS builder

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY package*.json ./

RUN npm ci

# Copy frontend source code
COPY . .

# Build production React application
RUN npm run build


# ============================================================
# STAGE 2 — Serve React application with Nginx
# ============================================================

FROM nginx:alpine

# Remove default Nginx website configuration
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy React production build
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy our SPA Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]