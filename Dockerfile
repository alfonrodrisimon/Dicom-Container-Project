# Image
FROM python:3.11.1

# Working directory
WORKDIR /usr/app/

# Copy requirements.txt
COPY requirements.txt /usr/app/

#  Execute commands
RUN pip3 install -r requirements.txt

# Copy all the source code
COPY . /usr/app

# Expose port
EXPOSE 11113/tcp

#CMD instruction should be used to run the software
CMD [ "python3", "source/mwl.py"]