# tables.py
# TODO: Need to mirgate all the queries in this file and then clean them up. DRY!! 

from .models import Monster_Image, \
                    Monster, \
                    Researcher, \
                    Sighting, \
                    MonsterReport   

import logging

logger = logging.getLogger(__name__)
djangologger = logging.getLogger('django')

def IndexQuery():
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
                "path" : report.report,
                "researchers" : set(researchers_list),
                "monsters" : set(monsters_list),
                "sigthinglen" : counter 
            })
    logging.debug("Collect the selected report data into a dictionary for the view") 
    return { "reports": reports_list, "report_num": report_counter }

def GetTotalNumberOfReports():
    data = MonsterReport.objects.all().count()
    logging.debug(f"Counts all monster reports: {data}")
    return data

def GetAllMonsterReports():
    data = MonsterReport.objects.all()
    logging.debug(f"Grabed all monster reports: {data.values()}")
    return {'data': data.values()}

def GetAllSightings():
    data = Sighting.objects.all()
    logging.debug(f"Grabed all sightings: {data.values()}")
    return {'data': data.values()}

def GetAllResearchers():
    data = Researcher.objects.all()
    logging.debug(f"Grabed all researchers: {data.values()}")
    return {'data': data.values()}

def GetAllMonsters():
    data = Monster.objects.all()
    logging.debug(f"Grabed all monsters: {data.values()}")
    return {'data': data.values()}

def GetAllMonster_Images():
    data = Monster_Image.objects.all()
    logging.debug(f"Grabed all monster images: {data.values()}")
    return {'data': data.values()}