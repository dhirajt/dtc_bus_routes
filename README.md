dtc-bus-routes
==============

A web app to help you commute in Delhi!

**Project Home**  :  http://dhirajthakur.pythonanywhere.com/

This project is inspired from http://busroutes.in and of course <br />
the official site of DTC http://delhigovt.nic.in/dtcbusroute/dtc/Find_Route/getroute.asp !


How to run
==========

1. Install [pip](http://www.pip-installer.org/) and [virtualenv](http://www.virtualenv.org/)

        $ sudo apt-get install python-pip python-dev build-essential 
        $ sudo pip install --upgrade pip 
        $ sudo pip install --upgrade virtualenv 
        
2. Clone the repo, cd into it and run these commands to create a virtual environment
        
        ../dtc-bus-routes $ virtualenv venv             # creates a virtual environment
        ../dtc-bus-routes $ source venv/bin/activate    # activate it
        ../dtc-bus-routes $ deactivate                  # deactivate it when you are done

3. Install the dependencies of the project

        (venv) ../dtc-bus-routes $ pip install -r requirements.txt
        
4. Set these fields according to your database in **dtcbusroutes/settings.py**                                           
        
           'ENGINE': 'django.db.backends.',
           'NAME': '',
           'USER': '',
           'PASSWORD': ''

5. Run these commands to create necessary tables and load initial data

        ../dtc-bus-routes $ python manage.py syncdb                   # creates tables in db
        ../dtc-bus-routes $ python manage.py loaddata stage.json      # load initial data through json files
        ../dtc-bus-routes $ python manage.py loaddata route.json      # from rost/fixtures
        ../dtc-bus-routes $ python manage.py loaddata stageseq.json

6. Run the development server 

        ../dtc-bus-routes $ python manage.py runserver
  
  Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to run the site.
  
  
How to contribute
=================

You can contribute to code of the website by forking it and sending me a pull request after making changes
or you can suggest features, report bugs here on github or on [Facebook](http://www.facebook.com/dtcbusroutes) or
on [Twitter](https://twitter.com/#!/dhirajthakur92).

LICENSE
=======

This project is licenced under [GNU GPLv3 License](https://github.com/dhirajt/dtc-bus-routes/blob/master/LICENSE).

