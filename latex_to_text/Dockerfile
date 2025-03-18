# Base image
FROM node:18-alpine

# Set working directory to /app/latex_to_text
WORKDIR /app/latex_to_text

# Copy package.json and install dependencies
COPY latex_to_text/package*.json ./
RUN npm ci --only=production

# Copy the rest of the application code
COPY latex_to_text .

# Expose the port Node.js runs on
EXPOSE 3000

# Command to start the application
CMD ["npm", "start"]