FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# define the port number the container should expose
EXPOSE 8000

# run the command
# CMD [ "python", "-m" ,"wackywango.server","run-server", "rabbitmq://127.0.0.1:5672/", "-h", "127.0.0.1", "-p","8000"]

