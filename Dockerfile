# Image
FROM python:3.11.1

# Working directory
WORKDIR /usr/app/

#to COPY the remote file at working directory in container
COPY *.* /usr/app/

#  Execute commands
RUN pip3 install -r requirements.txt

#CMD instruction should be used to run the software
CMD [ "python3", "./source/mwl.py"]