# Use an official Python runtime as the base image
FROM python:3.9.17

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR NLPAtlas/

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY /NLPAtlas .

# Apply database migrations
RUN python manage.py migrate

# Expose the port that your Django app will run on
EXPOSE 8080

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
