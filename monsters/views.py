# pylint: disable=no-member

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
import csv

import logging

logger = logging.getLogger(__name__)

#Import models
from .models import Researcher
from .models import Monster
from .models import Sighting
from .models import MonsterReport

# Helper Functions

# Upload Helper
@login_required(login_url='/accounts/login')
def csv_uploader(myfile):
    # File upload #
    fs = FileSystemStorage() #Creates a insince of the FileSystemStorage class
    logging.info("File: {filename} was created in the file system!".format(filename=myfile.name))

    file = fs.save(myfile.name, myfile) #Save the file to the file system in the media folder in the monster app
    logging.info("File: {file_obj} was saved in the database!".format(file_obj=str(myfile)))
    
    uploaded_file_url = fs.url(file) # Gets the uploaded_file_url like
    filepath = fs.path(myfile.name) # Get the namefile with path
    file_name = myfile.name.split('.').pop(0) # Get the namefile without extension

    # Data upload #
    report = MonsterReport(title=file_name, filename=myfile.name, path=uploaded_file_url) #Creates a MonsterReport 
    report.save() #Save MonsterReport to the database 
    logging.debug("Report: {report_obj} was saved in the database!".format(report_obj=str(report)))

    # Opens the csv file and loops thur each item
    with open(filepath) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        #sighting = None
        for row in csv_reader:
            if line_count != 0:
                researcher = Researcher(name=row[1]) # Create a Researcher
                researcher.save() #Save Researcher to the database
                logging.debug("Researcher: {researcher_obj} was saved in the database!".format(researcher_obj=str(researcher)))   

                monster = Monster(name=row[2]) # Create a Monster
                monster.save() #Save Monster to the database
                logging.debug("Monster: {monster_obj} was saved in the database!".format(monster_obj=str(monster)))   

                # Create a Sighting
                sighting = Sighting(title='{}-sighting-{}'.format(file_name,line_count),
                                timestamp=row[0],
                                latitude=row[3],
                                longitude=row[4]
                                ) 
                sighting.save() #Save sighting to the database
                logging.debug("Sighting: {sighting_obj} was saved in the database!".format(sighting_obj=str(sighting)))

                sighting.researcher.add(researcher) #Add the relationship sighting to researcher to the database
                logging.debug("Researcher: {researcher_obj} was added in the database!".format(researcher_obj=str(researcher)))
                sighting.monster.add(monster) #Add the relationship sighting to monster to the database
                logging.debug("Monster: {monster_obj} was added in the database!".format(monster_obj=str(monster)))
                report.sighting.add(sighting) #Add the relationship MonsterReport to sighting to the database
                logging.debug("Sighting: {sighting_obj} was added in the database!".format(sighting_obj=str(sighting)))

            line_count += 1    
        logging.debug('Processed {} lines, upload file to files system and database'.format(line_count))   
        return('Processed {} lines, upload file to files system and database'.format(line_count))

# Create your views here.

# The General Views ('/':index.html, 
#                    '/report/<id>':report_details.html,
#                    '/report/sighting/<id>':sighting_details.html)
def index(request):
    """
    Displays the all MonsterReport on the index page
    """
    reports = MonsterReport.objects.all()
    logging.debug("Grabed all reports: {report_list}".format(report_list=str(reports)))
    reports_list = []
    
    report_counter = 0
    for report in reports.all(): #Grabs each report
        logging.debug("Grabed selected reports: {report_list}".format(report_list=str(report)))
        researchers_list, monsters_list = [], []
        researchers_dic, monsters_dic = {}, {}
        counter = 0
        
        for sight in report.sighting.all(): #Grabs each sighting for each report
            logging.debug("Grabed selected sightings by report: {sighting_list}".format(sighting_list=str(sight)))
            researchers_dic[sight.title] = [researcher.name for researcher in sight.researcher.all()] #Grabs each researcher in the sighting
            logging.debug("Grabed the titles of the selected resarchers: {researchers_dic}".format(researchers_dic=str(researchers_dic))) 
            monsters_dic[sight.title] = [monster.name for monster in sight.monster.all()] #Grabs each monster in the sighting
            logging.debug("Grabed the titles of the selected monsters: {monsters_dic}".format(monsters_dic=str(monsters_dic))) 
            researchers_list.append(' '.join(researchers_dic[sight.title])) #Change the dictionary into a string
            logging.debug("Change the dictionary into a string") 
            monsters_list.append(' '.join(monsters_dic[sight.title])) #Change the dictionary into a string
            logging.debug("Change the dictionary into a string") 

            counter = counter + 1        

            # Put a dictationary into a list to be used in the view
        report_counter = report_counter + 1
        reports_list.append({ 
                "id" : report.id,
                "title" : report.title,
                "filename" : report.filename,
                "path" : report.path,
                "researchers" : set(researchers_list),
                "monsters" : set(monsters_list),
                "sigthinglen" : counter 
            })
    logging.debug("Collect the selected report data into a dictionary for the view") 
    context = {
        "reports": reports_list,
        "report_num": report_counter,
        "user": request.user
    }

    return render(request, 'monsters/index.html', context)

def report_details(request, id):
    """
    Displays the MonsterReport based on its id 
    """
    logging.debug("id: {id} \n and request: {request}".format(id=id, request=request))
    if int(id) == 0:
        logging.info("Redirect to root")
        return redirect('/')

    try:
        report = MonsterReport.objects.get(id=id) #Grabs report by the given id from the passed header
        logging.debug("Grabs the selected report by id: {report}".format(report=str(report)))
        sighting = report.sighting.all() #Grabs each sighting for the report
        logging.debug("Grabs the selected sightings: {sighting}".format(sighting=str(sighting)))

        #Loops throught each sighting then create a dicationary then add each one into a list for use in the view
        sighting_list = []
        counter = 0
        for sight in sighting: 
            sighting_list.append({
            'id':sight.id,
            'title':sight.title,
            'monsters': set([monster.name for monster in sight.monster.all()]),
            'researchers': set([researcher.name for researcher in sight.researcher.all()])
            })
            logging.debug("Append the selected sightings data: {sighting_data}".format(sighting_data=str(sighting_list)))
            counter = counter + 1

        context = {
            'report': report,
            'sighting':sighting_list,
            'sighting_size': counter
        }
        logging.info("Render to report_details view")
        return render(request, 'monsters/report_details.html', context)
    except Exception as e:
        # Future spot for logging failures
        logging.error("Index page failed: {e}".format(e))
        logging.info("Redirect to root")
        return redirect('/')

def sighting_details(request, id):
    """
    Displays the Sighting based on its id 
    """
    logging.debug("id: {id} \n and request: {request}".format(id=id, request=request))
    if int(id) == 0:
        logging.info("Redirect to root")
        return redirect('/')
    try:
        sighting = Sighting.objects.get(id=id) #Grabs sightng by the given id from the passed header
        logging.debug("Grabs the selected sighting by id: {sighting}".format(sighting=str(sighting)))
        researchers = [researcher.name for researcher in sighting.researcher.all()] #Grabs all the reseachers in the giving sighting
        logging.debug("Grabs the select names for monsters by sighting: {sighting}".format(researchers=str(researchers)))
        monsters = [monster.name for monster in sighting.monster.all()] #Grabs all the monsters in the giving sighting
        logging.debug("Grabs the select names for monsters by sighting: {monsters}".format(monsters=str(monsters)))

        
        report = sighting.monsterreport_set # Gets the values form the parent monsterreport of the sighting
        # Grabs the values of report
        report_id = report.values("id").get()['id']
        report_title = report.values("title").get()['title']
        logging.debug("Grabs the report id: {id} and title: {title}".format(id=report_id,title=report_title))

        # Counter the number of the sighting
        sighting_len = Sighting.objects.count()

        context = {
            'sighting':sighting,
            'researchers': set(researchers),
            'monsters': set(monsters),
            'report_id': report_id,
            'report_title': report_title,
            'len': sighting_len
        }

        logging.info("Render the sighting details view")
        return render(request, 'monsters/sighting_details.html', context)
    except Exception as e:
        # Future spot for logging failures
        logging.error("Index page failed: {e}".format(e))
        logging.info("Redirect to root")
        return redirect('/')

# Upload sections ( '/report/upload/':upload.html )
@login_required(login_url='/accounts/login')
def upload_csv(request):
    """ 
    Uploads file to media folder and then readers the data from the uploaded file then inputs the file data into the database
    """
    # Checks if their is POST request and if it is passed a file
    message = ""
    logging.debug("Request method type: {method}".format(method=request.method))
    if request.method == 'POST':
        try:
            logging.debug("Tries to grab file")
            if strip_tags(request.FILES['myfile']):
                try:
                    myfile = strip_tags(request.FILES['myfile']) #Grabs the file
                    logging.debug("Grabs the files: {file} and strip tags".format(file=myfile))
                    if myfile.split('.').pop(1) != "csv":
                        raise AssertionError("Wrong filetype")
                    else: 
                        try:
                            message = csv_uploader(myfile)
                            return redirect('/')
                        except Exception as e:
                            logging.warning("File data upload error: {e}".format(e))
                            message = "ERROR: No File Data uploaded"
                except Exception as e:
                    logging.warning("File upload error: {e}".format(e))
                    message = "ERROR: No File uploaded - Wrong filetype {}".format(e)
        except Exception as e:
            logging.warning("File request error: {e}".format(e))
            message = "ERROR: No file request found"
    context = {
        'message': message,
    }
    return render(request, 'monsters/upload.html',context)

# Seaching Functions ('/search/researcher/<name>':search_researcher, 
#                     '/search/monster/<name>':search_monster,
#                     '/search/sighting/<title>':search_sighting, 
#                     '/search/report/<title>':search_report),
#                     '/search/sighting/<id>':search_sighting),
#                     '/search/report/<id>':search_report)
def search_researcher(request, name):
    """ search by researcher name and returns all sighting with reseacher name """
    name = " ".join(name.split("%20"))
    query = { 'type':"Researcher", "content":name}
    logging.debug("Grabs name: {name}, query: {query}".format(name=name,query=query))
    researchers = Researcher.objects.filter(name=name) #Grabs sightng by the given id from the passed header    
    logging.debug("Grabs reseachers filter by name - Researchers: {researchers}".format(researchers=str(researchers)))

    sighting_list = []
    counter = 0
    for researcher in researchers:
        sighting_list.append({
            'id': researcher.sighting_set.get().id,
            'title': researcher.sighting_set.get().title,
            'monsters': set([monster.name for monster in researcher.sighting_set.get().monster.all()]),
            'researchers': set([researcher.name for researcher in researcher.sighting_set.get().researcher.all()]),
        })
        counter = counter + 1    
    logging.debug("Grabs all the researchers and monsters data: {sighting_list}".format(sighting_list=str(sighting_list)))   

    context = {
        'query': query, 
        'results': sighting_list,
        'result_num': counter
    }
    return render(request, 'monsters/search_result.html', context)

def search_monster(request, name):
    """ search by monster name and returns all monster with monster name """
    name = " ".join(name.split("%20"))
    query = { 'type':"Monster", "content":name}
    logging.debug("Grabs name: {name}, query: {query}".format(name=name,query=query))
    monsters = Monster.objects.filter(name=name) #Grabs sightng by the given id from the passed header
    logging.debug("Grabs monsters filter by name - Monster: {monsters}".format(monsters=str(monsters)))    

    sighting_list = []
    counter = 0
    for monster in monsters:
        sighting_list.append({
            'id': monster.sighting_set.get().id,
            'title': monster.sighting_set.get().title,
            'monsters': set([monster.name for monster in monster.sighting_set.get().monster.all()]),
            'researchers': set([researcher.name for researcher in monster.sighting_set.get().researcher.all()]),
        })
        counter = counter + 1
    logging.debug("Grabs all the researchers and monsters data: {sighting_list}".format(sighting_list=str(sighting_list)))  

    context = {
        'query': query, 
        'results': sighting_list,
        'result_num': counter
    }
    return render(request, 'monsters/search_result.html', context)

def search_sighting_title(request, title):
    """ search by sighting title and returns all sighting with sighting title """
    title = " ".join(title.split("%20"))
    query = { 'type':"Sighting", "content":title}
    logging.debug("Grabs name: {title}, query: {query}".format(title=title,query=query))
    sightings = Sighting.objects.filter(title=title) #Grabs sightng by the given id from the passed header
    logging.debug("Grabs sightings filter by name - Sighting: {sightings}".format(sightings=str(sightings)))    


    sighting_list = []
    counter = 0
    for sighting in sightings:
        sighting_list.append({
            'id': sighting.id,
            'title': sighting.title,
            'monsters': set([monster.name for monster in sighting.monster.all()]),
            'researchers': set([researcher.name for researcher in sighting.researcher.all()]),
        })
        counter = counter + 1
    logging.debug("Grabs all the researchers and monsters data: {sighting_list}".format(sighting_list=str(sighting_list))) 

    context = {
        'query': query, 
        'results': sighting_list,
        'result_num': counter
    }
    return render(request, 'monsters/search_result.html', context)

def search_report_title(request, title):
    """ search by report title and returns all report with report title """
    title = " ".join(title.split("%20"))
    query = { 'type':"Report", "content":title}
    logging.debug("Grabs name: {title}, query: {query}".format(title=title,query=query))
    reports = MonsterReport.objects.filter(title=title) #Grabs sightng by the given id from the passed header
    logging.debug("Grabs reports filter by name - MonsterReport: {reports}".format(reports=str(reports)))   

    sighting_list = []
    counter = 0
    for report in reports:
        for sighting in report.sighting.all():
            sighting_list.append({
                'id': sighting.id,
                'title': sighting.title,
                'monsters': set([monster.name for monster in sighting.monster.all()]),
                'researchers': set([researcher.name for researcher in sighting.researcher.all()]),
            })
            counter = counter + 1
    logging.debug("Grabs all the researchers and monsters data: {sighting_list}".format(sighting_list=str(sighting_list))) 

    context = {
        'query': query, 
        'results': sighting_list,
        'result_num': counter
    }
    return render(request, 'monsters/search_result.html', context)

def search_sighting_id(request, id):
    """ search by sighting id and redirect to sighting with sighting id """
    logging.debug("Current request: {request}, id: {id}".format(request=request,id=id))
    return redirect('/report/sighting/{}'.format(id))

def search_report_id(request, id):
    """ search by report id and redirect to report with report id """
    logging.debug("Current request: {request}, id: {id}".format(request=request,id=id))
    return redirect('/report/{}'.format(id))

def login_view(request):
    logging.debug("Request method type: {method}".format(method=request.method))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logging.info("Redirect to root")
            return redirect('/')
        else:
            logging.info("Render login view")
            return render(request, 'monsters/login.html')
    logging.info("Render login view")
    return render(request, 'monsters/login.html')

def logout_view(request):
    logout(request)
    logging.info("Redirect to root")
    return redirect('/')