# Multi-stage build
FROM node:18-alpine as build-stage

ARG ENV_STR

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with clean install for production
RUN npm install && npm cache clean --force

# Copy source code
COPY . .

RUN echo $ENV_STR > .env

RUN cat .env

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine as production-stage

# Copy custom nginx config (optional)
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application from build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# # Add non-root user for security
# RUN addgroup -g 1001 -S nodejs && \
#     adduser -S viteuser -u 1001

# # Set proper permissions
# RUN chown -R viteuser:nodejs /usr/share/nginx/html && \
#     chown -R viteuser:nodejs /var/cache/nginx && \
#     chown -R viteuser:nodejs /var/log/nginx && \
#     chown -R viteuser:nodejs /etc/nginx/conf.d

# # Switch to non-root user
# USER viteuser

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]