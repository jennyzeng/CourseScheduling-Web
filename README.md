# README a ggod project

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
You should remove old course and requirements data in the old version before doing the following operations.

You can manage your data in database using [Robo 3T](https://robomongo.org/).

### Option1: Upload from Admin

URL: [http://localhost:8000/admin/upload/](http://localhost:8000/admin/upload/)
```
admin username: admin  
admin password: admin
```

#### Step1:

Upload Courses

- Select 'Courses' in the selectbox
- Choose json files in the database/courses/ folder, and upload them one by one.

#### Step2:

Upload Requirements

- Select  'Requirements' in the selectbox
- Choose json files in the database/requirements/ folder, and upload them one by one.

### Option2: Upload in terminal

When our services are running, in another terminal, do

```
# To load course: 

docker-compose exec website python database/manage.py load_course -f [path-to-the-file] 

# To load requirements:
# general:
docker-compose exec website python database/manage.py load_requirement -f [path-to-the-file]

## for universial
docker-compose exec website python database/manage.py load_requirement -f database/requirements/UNIVERSAL.json

## cs major:
docker-compose exec website python database/manage.py load_requirement -f "database/requirements/COMPUTER SCIENCE.json" 
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

## XML parsing 

Parsing student id and name are easy, but parsing requirements that student has completed and computing how many courses away from completion from degreework is hard.

basic structure

1,  
```                        
                            rule 
 	       
 	         /                |              \           \

      requirement           rule             rule		... (mutiple rules)
   (self-defining tag                    
    describing how many
    rules to pick)
```
2,    
```                   
                         rule
 
		    /             |                \       
    classes_applied      ...            requirement (attr : classes_begin)
                                       /      |      \
                                  course    course   ...
```

## Reference

[udemy: build a SAAS app with flask](https://www.udemy.com/the-build-a-saas-app-with-flask-course)
