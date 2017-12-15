# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /API
WORKDIR /API

# Install any needed packages specified in requirements.txt
ADD requirements.txt /API
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /API
ADD . /API

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run gotg-api.py when the container launches
CMD ["python", "gotg-api.py"]
