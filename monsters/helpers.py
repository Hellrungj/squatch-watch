# pylint: disable=no-member
from django.core.files.storage import FileSystemStorage
import csv
import logging

logger = logging.getLogger(__name__)
djangologger = logging.getLogger('django')

# Import models
from .models import Researcher
from .models import Monster
from .models import Sighting
from .models import MonsterReport    

# Helper Functions

# Upload Helper
def csv_uploader(myfile):
    logging.info("File: {file} ".format(file=myfile))
    # File upload #
    
    return("Ran csv_uploader")
    
    fs = FileSystemStorage()

    filename = fs.save(myfile.name, myfile) #Save the file to the file system in the media folder in the monster app
    logging.info("File: {file_obj} was saved in the database!".format(file_obj=myfile.name))
    
    uploaded_file_url = fs.url(filename) # Gets the uploaded_file_url like
    filepath = fs.path(filename) # Get the namefile with path
    #file_name = myfile.split('.').pop(0) # Get the namefile without extension
    print(myfile.name)
    # Data upload #
    report = MonsterReport(title=filename, filename=myfile.name, path=uploaded_file_url) #Creates a MonsterReport 
    report.save() #Save MonsterReport to the database 
    logging.debug("Report: {report_obj} was saved in the database!".format(report_obj=str(report)))

    # Opens the csv file and loops thur each item
    with open(filepath) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0                       
        sighting = None
        for row in csv_reader:
            if line_count != 0:
                researcher = Researcher(name=row[1]) # Create a Researcher
                researcher.save() #Save Researcher to the database
                logging.debug("Researcher: {researcher_obj} was saved in the database!".format(researcher_obj=str(researcher)))   

                monster = Monster(name=row[2]) # Create a Monster
                monster.save() #Save Monster to the database
                logging.debug("Monster: {monster_obj} was saved in the database!".format(monster_obj=str(monster)))   

                # Create a Sighting
                sighting = Sighting(title='{}-sighting-{}'.format(filename,line_count),
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



def csvimport(file):
    fpath = file.url
    #THIS IS DONE BECAUSE file.url gives a 
    #path which has forward slashes
    #and system I am using is windows
    #and it's directory uses backward slash
    if(BASE_DIR.find('\\')==1):
        fpath = fpath.replace('/','\\')
    #REMOVE ABOVE LINE IF YOU ARE WORKING IN LINUX

    path = BASE_DIR + fpath
    f = open(path,'rt')
    reader = csv.reader(f)
    for row in reader:
        _, created = Teacher.objects.get_or_create(
        first_name=row[0],
        last_name=row[1],
        middle_name=row[2],
        )