# README

## Set up

```
git clone https://github.com/jennyzeng/CourseScheduling-Web.git
```

### Database

install [MongoDB](https://www.mongodb.com/)

```
# go to the repo dir
$ cd CourseScheduling-Web
# make directory for MongoDB
$ mkdir -p ./data/db
# run MongoDB using the db path we just created
$ mongod -dbpath ./data
```

### Python installation
install [python 3.6](https://www.python.org/) 

create python3.6 virtual env called `flask` in the repo directory
```
# activate the virtual env
$ source activate ./flask/bin/activate
# install packages
(flask) $ flask/bin/pip install -r ./requirements.txt
```

### flask
to be continue...

## Reference

- https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
- http://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_RESTAPI_with_Flask.php
