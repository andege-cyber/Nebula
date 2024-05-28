# Use a base image
FROM nginx:alpine

# Set the working directory
WORKDIR /usr/share/nginx/html

# Copy the necessary files to the container
COPY . .

#assigning appropriate permissions for our file to be read by Nginx
RUN chmod -R 755 /usr/share/nginx/html

# Expose a port
EXPOSE 8080

# Start the nginx server
CMD ["nginx", "-g", "daemon off;"]