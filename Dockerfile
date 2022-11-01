
# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /home/realuser

# Set the working directory to /realuser
WORKDIR /home/realuser

RUN groupadd -r realuser && useradd -r -g realuser realuser



USER realuser


# Copy the current directory contents into the container at /realuser
COPY . /home/realuser

RUN chown -R realuser:realuser /home/realuser/start.sh
# Install any needed packages specified in requirements.txt
RUN export PATH="$HOME/.local/bin:$PATH"  && pip install -r requirements.txt




RUN chmod +x /home/realuser/start.sh
