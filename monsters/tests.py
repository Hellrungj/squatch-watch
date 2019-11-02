from django.test import TestCase
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.http import urlencode

from . import views
import datetime
import random
import os
import csv

from .models import Researcher
from .models import Monster
from .models import Sighting
from .models import MonsterReport


def creates_monster(monster_name="Nelly"):
    """ Creates a monster and saves it in the database"""
    monster = Monster(name=monster_name)
    monster.save()
    return monster

def creates_reseacher(reseacher_name="John"):
    """ Creates a reseacher and saves it in the database"""
    researcher = Researcher(name=reseacher_name)
    researcher.save()
    return researcher

def creates_sighting(title='Hello',timestamp="2018-01-01 12:53:59",latitude=12.5,longitude=0.5,monster=creates_monster(),researcher=creates_reseacher()):
    """ Creates a sighting and saves it in the database"""
    sighting = Sighting(title=title,timestamp=timestamp,latitude=latitude,longitude=longitude)
    sighting.save()
    sighting.monster.add(monster)
    sighting.researcher.add(researcher)
    return sighting

def creates_monster_report(title="First",filename="First.csv",path="/media/First/csv",sighting=creates_sighting()):
    """ Creates a monster report and saves it in the database"""
    monster_report = MonsterReport(title=title,filename=filename,path=path)
    monster_report.save()
    monster_report.sighting.add(sighting)
    return monster_report

def store_file_in_database(self,filename='one.csv'):
    """ Opens the one.csv file then stores it the database """
    fs = FileSystemStorage()
    filepath = fs.path(filename) # Get the namefile with path


    with open(filepath) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                researcher= creates_reseacher(name=row[1])
                monster= creates_monster(name=row[2])
                sight = creates_sighting(
                    title='{}-sighting-{}'.format(filename,line_count),
                    timestamp=row[0],
                    latitude=row[3],
                    longitude=row[4],
                    researcher=researcher,
                    monster=monster
                                    ) 
                creates_monster_report(sighting=sight)     

class ModelsTests(TestCase):
    def test_monster_creation(self):
        """ Creates monster then test if monster in the database """
        monster = creates_monster()
        self.assertEqual(monster.id, 1)
        monster2 = Monster.objects.get(id=1)
        self.assertEqual(monster.name, monster2.name)

    def test_reseacher_creation(self):
        """ Creates researcher then test if researcher in the database """
        reseacher = creates_reseacher()
        self.assertEqual(reseacher.id, 1)
        researcher2 = Researcher.objects.get(id=1)
        self.assertEqual(reseacher.name, researcher2.name)

    def test_sighting_creation(self):
        """ Creates sighting then test if sighting in the database """
        sight = creates_sighting()
        self.assertEqual(sight.id, 1)
        sighting = Sighting.objects.get(id=1)

        self.assertEqual(sight.title, sighting.title)
        #self.assertQuerysetEqual(sight.monster.values(), sighting.monster.values())
        #self.assertQuerysetEqual(sight.researcher.values(), sighting.researcher.values())
        self.assertEqual(sight.latitude, sighting.latitude)
        self.assertEqual(sight.longitude, sighting.longitude)

    def test_monster_report_creation(self):
        """ Creates MonsterReport then test if MonsterReport in the database """
        report = creates_monster_report(sighting=creates_sighting(researcher=creates_reseacher(),monster=creates_monster()))
        self.assertEqual(report.id, 1)
        monster_report = MonsterReport.objects.get(id=1)
        
        self.assertEqual(report.title, monster_report.title)
        self.assertEqual(report.filename, monster_report.filename)
        self.assertEqual(report.path, monster_report.path)
        #self.assertQuerysetEqual(report.sighting.values(), monster_report.sighting.values())

# File Uploads Tests
class FileUploadTest(TestCase):
    def test_upload_view(self):
        """ Gets the response then checks the status code and context of the response being send back from the view """
        response = self.client.get('/report/upload/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'],"")

    def test_upload_with_no_file_in_request(self):
        """ Gets the response then checks the status code and context of the response being send back from the view """
        response = self.client.post('/report/upload/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'],"ERROR: No file request found")

    def test_upload_with_no_file_data(self):
        """ Gets the response then checks the status code and context of the response being send back from the view """
        response = self.client.post('/report/upload/', {'myfile': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'],"ERROR: No file request found")


    def test_upload_with_bad_sample_file(self):
        """ Gets grabs a file and then adds the file to post then gets response and then the checks the status code and context of the response being send back from the view """
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, '../sample/bad.csv')
        file = open(file_path,'r')
        response = self.client.post('/report/upload/', {'myfile': file})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'],"ERROR: No File Data uploaded")

    def test_upload_with_good_sample_file(self):
        """ Gets grabs a file and then adds the file to post then gets response and then the checks the status code and context of the response being send back from the view """
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, '../sample/one.csv')
        file = open(file_path,'r')
        response = self.client.post('/report/upload/', {'myfile': file})

        self.assertEqual(response.status_code, 302)

        #Testing if file in media dir
        file_path = os.path.join(module_dir, '../media/one.csv')
        self.assertEqual(os.path.exists(file_path),True)

        #Testing Database for data
        #Grabs the report data
        monster_report = MonsterReport.objects.get(filename='one.csv')
        # Grabs first sighting the report
        sighting = monster_report.sighting.all()[0]
        monster = sighting.monster.all()[0]
        researcher = sighting.researcher.all()[0]
        # Tests the first sighting of the report
        self.assertEqual(monster_report.title, 'one')
        self.assertEqual(sighting.title, 'one-sighting-1')
        self.assertEqual(sighting.latitude, 48.689912)
        self.assertEqual(sighting.longitude, -121.636151)
        self.assertEqual(researcher.name, 'Bingo Jenkins')
        self.assertEqual(monster.name, 'Bigfoot')

        # Grabs last sighting the report
        sighting = monster_report.sighting.all()[16]
        monster = sighting.monster.all()[0]
        researcher = sighting.researcher.all()[0]
        # Tests the last sighting of the report
        self.assertEqual(monster_report.title, 'one')
        self.assertEqual(sighting.title, 'one-sighting-17')
        self.assertEqual(sighting.latitude, 34.101372)
        self.assertEqual(sighting.longitude, -116.088088)
        self.assertEqual(researcher.name, 'Missy Jorgensen')
        self.assertEqual(monster.name, 'Sand Zombie')

# Views Tests
class IndexViewTests(TestCase):
    def test_index_views_with_no_monsterreports(self):
        """ Gets the response then checks the status code and context of the response being send back from the view """
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['reports'], [])
        self.assertEqual(response.context['report_num'], 0)

    def test_index_views_with_monsterreports_data(self):
        """ Creates a full monster report and gets the response then checks the status code and context of the response being send back from the view """
        creates_monster_report(sighting=creates_sighting(researcher=creates_reseacher(),monster=creates_monster()))
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['reports'],
            [{'researchers': {'John'}, 'sigthinglen': 1, 'id': 1,
              'monsters': {'Nelly'}, 'title': 'First',
              'path': '/media/First/csv', 'filename': 'First.csv'}]
        )
        self.assertEqual(response.context['report_num'], 1)

        

class ReportDetailsViewTests(TestCase):
    def test_report_details_views_with_no_monsterreports(self):
        """ Gets the response then checks the status code and context of the response being send back from the view """
        response = self.client.get('/report/{}/'.format(random.randrange(0,1000,1)))

        self.assertEqual(response.status_code, 302)

    def test_report_details_views_with_no_monsterreports_takes_incoming_str_not_int(self):
        """ Gets the response then checks the status code and context of the response being send back from the view """
        response = self.client.get('/report/{}/'.format("Test"))

        self.assertEqual(response.status_code, 404)

    def test_report_detail_views_with_monsterreports(self):
        """ Creates a full monster report and gets the response then checks the status code and context of the response being send back from the view """
        report = creates_monster_report(sighting=creates_sighting(researcher=creates_reseacher(),monster=creates_monster()))
        response = self.client.get('/report/{}/'.format(report.id))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['report'], report)
        self.assertEqual(response.context['sighting'], [
                                {'id': 1, 'monsters': {'Nelly'},
                                 'researchers': {'John'}, 'title': 'Hello'}])
        self.assertEqual(response.context['sighting_size'], 1)

        

class SightingDetailsViewTests(TestCase):
    """ Gets the response then checks the status code and context of the response being send back from the view """
    def test_sighting_details_views_with_no_monsterreports(self):
        response = self.client.get('/report/sighting/{}/'.format(random.randrange(0,1000,1)))

        self.assertEqual(response.status_code, 302)

    def test_sighting_details_views_with_no_monsterreports_takes_incoming_str_not_int(self):
        """ Gets the response then checks the status code and context of the response being send back from the view """
        response = self.client.get('/report/sighting/{}/'.format("Test"))

        self.assertEqual(response.status_code, 404)
    

    def test_sighting_details_views_with_monsterreports(self):
        """ Creates a full monster report and gets the response then checks the status code and context of the response being send back from the view """
        sighting=creates_sighting(monster=creates_monster(),researcher=creates_reseacher())
        creates_monster_report(sighting=sighting)
        response = self.client.get('/report/sighting/{}/'.format(sighting.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sighting'],sighting)
        self.assertEqual(response.context['researchers'],{'John'})
        self.assertEqual(response.context['monsters'],{'Nelly'})
        self.assertEqual(response.context['report_id'],1)
        self.assertEqual(response.context['report_title'], "First")
        self.assertEqual(response.context['len'],1)

# Seaching Functions ('/search/researcher/<name>':search_researcher, 
#                     '/search/monster/<name>':search_monster,
#                     '/search/sighting/<title>':search_sighting, 
#                     '/search/report/<title>':search_report),
#                     '/search/sighting/<id>':search_sighting),
#                     '/search/report/<id>':search_report)

class SearchViewTests(TestCase):
    def test_search_for_report_id(self):
        """ Creates a full monster report and gets the response then checks the status code and context of the response being send back from the view """
        report = creates_monster_report(sighting=creates_sighting(researcher=creates_reseacher(),monster=creates_monster()))
        response = self.client.get('/search/report/{}/'.format(report.id))

        self.assertEqual(response.status_code, 302)

    def test_search_for_sighting_id(self):
        """ Creates a full monster report and gets the response then checks the status code and context of the response being send back from the view """
        sighting=creates_sighting(researcher=creates_reseacher(),monster=creates_monster())
        report = creates_monster_report(sighting=sighting)
        response = self.client.get('/search/sighting/{}/'.format(sighting.id))

        self.assertEqual(response.status_code, 302)

    def test_search_for_report_title(self):
        """ Creates a full monster report and gets the response then checks the status code and context of the response being send back from the view """
        report = creates_monster_report(sighting=creates_sighting(researcher=creates_reseacher(),monster=creates_monster()))
        response = self.client.get('/search/report/{}/'.format(report.title))

        self.assertEqual(response.status_code, 200)

    def test_search_for_sighting_title(self):
        """ Creates a full monster report and gets the response then checks the status code and context of the response being send back from the view """
        sighting=creates_sighting(researcher=creates_reseacher(),monster=creates_monster())
        report = creates_monster_report(sighting=sighting)
        response = self.client.get('/search/sighting/{}/'.format(sighting.title))

        self.assertEqual(response.status_code, 200)

    def test_search_for_reseacher(self):
        """ Creates a full monster report and gets the response then checks the status code and context of the response being send back from the view """
        researcher=creates_reseacher()
        sighting=creates_sighting(researcher=researcher,monster=creates_monster())
        report = creates_monster_report(sighting=sighting)
        response = self.client.get('/search/researcher/{}/'.format(researcher.name))

        self.assertEqual(response.status_code, 200)

    def test_search_for_monster(self):
        """ Creates a full monster report and gets the response then checks the status code and context of the response being send back from the view """
        monster=creates_monster()
        sighting=creates_sighting(researcher=creates_reseacher(),monster=monster)
        report = creates_monster_report(sighting=sighting)
        response = self.client.get('/search/monster/{}/'.format(monster.name))

        self.assertEqual(response.status_code, 200)