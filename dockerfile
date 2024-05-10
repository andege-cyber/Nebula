# Use a base image
FROM nginx:alpine

# Set the working directory
WORKDIR /usr/share/nginx/html

# Copy the necessary files to the container
COPY . .

# Expose a port
EXPOSE 5000

# Start the nginx server
CMD ["nginx", "-g", "daemon off;"]
