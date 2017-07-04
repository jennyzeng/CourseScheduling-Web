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
to stop 

some other related operations:

```
# Remove stopped containers
docker-compose rm -f
# Remove "dangling" images
docker rmi -f $(docker images -qf dangling=true)
```

## about testing
first, use `docker-compose up` to run the container,
then in another terminal, 
do 

```
$ docker-compose exec website py.test CourseScheduling/tests
```
or 

```
$ docker-compose exec website py.test --cov-report term-missing --cov
```