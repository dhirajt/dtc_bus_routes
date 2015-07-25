dtc_bus_routes
==============

A web app to help you commute in Delhi!

**Project Home**  :  http://www.dtcbusroutes.in/

This project is inspired from http://busroutes.in (http://web.archive.org/web/20130424050914/http://busroutes.in/chennai/) and of course <br />
the official site of DTC http://delhigovt.nic.in/dtcbusroute/dtc/Find_Route/getroute.asp !


How to run
==========

1. Install [pip](http://www.pip-installer.org/) and [virtualenv](http://www.virtualenv.org/)
   (Instructions are for debian systems, if you use RedHat/Fedora etc. search for respective package managers.)

        $ sudo apt-get install python-pip python-dev build-essential 
        $ sudo pip install --upgrade pip 
        $ sudo pip install --upgrade virtualenv 
        
2. Clone the repo, cd into it and run these commands to create a virtual environment
        
        ../dtc_bus_routes $ virtualenv venv             # creates a virtual environment
        ../dtc_bus_routes $ source venv/bin/activate    # activate it
        ... run the project steps 3,4,5,6 etc ... 
        ../dtc_bus_routes $ deactivate                  # deactivate it when you are done running the project

3. Install the dependencies of the project

        (venv) ../dtc_bus_routes $ pip install -r requirements/local.txt
        
4. Set the 'DATABASE_URL' according to your database in the environment.
    
        For example: 
        ../dtc_bus_routes $ export DATABASE_URL="postgresql://dbuser:dbRANDOMPASSWORD@localhost/dtc_bus_routes"

5. Run these commands to create necessary tables and load initial data

        ../dtc_bus_routes $ python manage.py migrate                   # creates tables in db
        ../dtc_bus_routes $ python manage.py loaddata stage.json      # load initial data through json files
        ../dtc_bus_routes $ python manage.py loaddata route.json      # from busroutes/fixtures
        ../dtc_bus_routes $ python manage.py loaddata stageseq.json

6. Run the development server 

        ../dtc_bus_routes $ python manage.py runserver
  
  Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to run the site.
  
  
How to contribute
=================

You can contribute to code of the website by forking it and sending me a pull request after making changes
or you can suggest features, report bugs here on github or on [Facebook](http://www.facebook.com/dtcbusroutes) or
on [Twitter](https://twitter.com/#!/dhirajthakur92).

LICENSE
=======

This project is licenced under [GNU GPLv3 License](https://github.com/dhirajt/dtc-bus-routes/blob/master/LICENSE).

