FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the app
COPY . .

# Disable telemetry
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000

# Build the app
RUN npm run build

# Expose the port
EXPOSE 3000

# Start production server
CMD ["npm", "run", "start"]
