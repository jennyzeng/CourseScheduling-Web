# README

## Set up

```
git clone https://github.com/jennyzeng/CourseScheduling-Web.git
```

install Docker at [https://www.docker.com/](https://www.docker.com/)

Then, `cd` to the repo, run

```
$ docker-compose up --build
```

you will see the demo page at [http://localhost:8000/](http://localhost:8000/)

after that you can run 

```
$ docker-compose up
```

to start it, and 
```
$ docker-compose down
```
to stop. Note that use Ctrl-C to stop the service after you enter `docker-compose up` does not stop it, so
you should do `docker-compose down` to ensure it is not running anymore actually.

some other related operations:

```
# Remove stopped containers
docker-compose rm -f
# Remove "dangling" images
docker rmi -f $(docker images -qf dangling=true)
```
## load sample data to database
When our services are running, in another terminal, do

```
# To load course: 

docker-compose exec website python database/manage.py load_course -f [path-to-the-file] 

# To load requirements with major:
# general:
docker-compose exec website python database/manage.py load_requirement -n [major-name] -f [path-to-the-file]

## for universial
docker-compose exec website python database/manage.py load_requirement

## cs major:
docker-compose exec website python database/manage.py load_requirement -n "Computer Science" -f "database/txt_files/cs.txt" 
```
remember that if you want to access the database in docker, the host name is the name of the database container name. 
That is, 'mongodb' in our case (You can see it in docker-compose.yml). 


## New Crawler that save courses as json file

```
docker-compose exec website python database/WebSoc.py
```
dept list and save path can be edited in database/WebSoc.py main

## about testing

write tests in CourseScheduling/tests, following the test pattern in page folder.

To test, use `docker-compose up` to run services,
then in another terminal, 
do 

```
$ docker-compose exec website CourseScheduling test
```
or 

```
$ docker-compose exec website CourseScheduling conv
```

## Models

Course

Requirement
- SubSreq

Major
- Requirement

## Reference

[udemy: build a SAAS app with flask](https://www.udemy.com/the-build-a-saas-app-with-flask-course)