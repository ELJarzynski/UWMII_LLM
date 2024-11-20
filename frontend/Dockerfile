FROM node:16

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Install axios for Vue.js
RUN npm install axios

# Copy the rest of the application
COPY . .

# Command to run the application in development mode
CMD ["npm", "run", "dev"]