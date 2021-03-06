dev_env
=======

Created By Dan Sheffner
-----------------------


overview
~~~~~~~~~~~~~

docker-compose.yml
    | dev_env with python/ipython/junipter notebooks
    | contains a postgres server

helper.py
    | a script to manage docker containers

setup.ipynb
    | a default example of how to use ipython with sqlalchemy

default directory structure:
    | ~/ipython/postgres - postgres data
    | ~/ipython/images   - docker save location
    | ~/ipython/data     - directory mapped into the notebook docker container

To run:
::
    $ git clone https://github.com/thesheff17/dev_env.git
    $ mkdir -p ~/ipython/data ~/ipython/images ~/ipython/postgres
    $ cp ./setup.ipynb ~/ipython/data/
    $ docker-compose up
    $ # The terminal will spit out a url like this: http://localhost:8888/?token=

To stop:
::
    $ # ctrl-c in the docker-compose up window or
    $ docker-compose down

