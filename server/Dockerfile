# Use the official Python base image
FROM python:3.12.0-slim-bookworm

# Set environment variables to improve performance and disable bytecode generation
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# Define the application directory
ENV APP=/app

# Change the working directory to the application directory
WORKDIR $APP

# Copy the requirements.txt file to the application directory
COPY requirements.txt $APP

# Install Python dependencies from requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy the rest of the application files to the container
COPY . $APP

# Expose the port that the application will run on
EXPOSE 8000

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Specify the entrypoint script to run when the container starts
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Define the default command to start the application using Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
