dev_env
=======

Created By Dan Sheffner
-----------------------


overview
~~~~~~~~~~~~~
::
    docker-compose.yml - dev_env with python/ipython/junipter notebooks
                       - contains a postgres server
    helper.py          - a script to manage docker containers
    setup.ipynb        - a default example of how to use ipython with sqlalchemy

    This setup assumes some default directories to remember state with docker
    ~/ipython/postgres - postgres data
    ~/ipython/images   - docker save location
    ~/ipython/data     - mapped directory for the notebooks

To run:
::
    $ git clone https://github.com/thesheff17/dev_env.git
    $ mkdir -p ~/ipython/data ~/ipython/images ~/ipython/postgres
    $ cp ./setup.ipynb ~/ipython/data/
    $ docker-compose up

