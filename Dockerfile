FROM python:3.8-slim-buster

LABEL maintainer="dev.lucasmartins@gmail.com"

# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app

# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP
WORKDIR $APP

# Expose the port uWSGI will listen on
EXPOSE 5000

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# We copy the rest of the codebase into the image
COPY . .

ENTRYPOINT ["python"]

CMD ["web.py"]
