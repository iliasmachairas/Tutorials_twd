# Use a Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

## Copy the requirements.txt file to the container
COPY requirements.txt .
#
## Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Specify the command to run when the container starts
CMD [ "python", "main.py" ]
