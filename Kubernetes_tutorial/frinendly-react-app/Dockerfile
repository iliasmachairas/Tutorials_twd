# Step 1: Use official Node.js image as the base
FROM node:18 AS build

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy package.json and package-lock.json to the container
COPY package*.json ./
# it will copy all the depndencies - fater re-build 

# Step 4: Install dependencies
RUN npm install

# Step 5: Copy the rest of the app's source code to the container
COPY . .

# Step 6: Build the app for production
RUN npm run build

# Step 7: Use a smaller image (Nginx) to serve the build folder
FROM nginx:alpine

# Step 8: Copy the build output to Nginx's default directory
#COPY --from=build /app/build /usr/share/nginx/html # for react app - next line - vite app
COPY --from=build /app/dist /usr/share/nginx/html
# ---from=build refers to previous step
# copies the only the build files from dist 

# Step 9: Expose port 80 (default HTTP port)
EXPOSE 80

# Step 10: Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]

# explanation first layes to build final files
# last aprt to serve these files 