# SQUATCH WATCH

*The truth is in here.*

### Introduction

The point of this bare-bones application is to display basic data related to cryptozoological findings in a single place that is easy to view and query by researchers. Sighting data is added to the system in the form of "reports" – CSV files containing rows for individual sightings. The functionality of the app can be broken into two main components:
- An **HTTP endpoint** that handles requests with a CSV file payload and creates objects for the application from the file
- A **front-end table** that displays all sightings created from CSV data and can be filtered by monster, researcher, or specific report

Additionally, in order to submit data to the application, a separate **HTTP client** (`http_client.py`) is provided to look for files in a directory and send them to the HTTP endpoint.

### Data and schema

Each CSV file contains a row per monster sighting being reported by a researcher. The CSV format is as follows:

```
#"timestamp","researcher","monster","latitude","longitude"
"2018-01-01 23:59:59","Jonathan Barker","Dracula","46.8999964","24.1499994"
```

When a file is submitted, it creates objects that correspond with the application's four models:
- `MonsterReport`: refers to a single CSV report that is comprised of many sightings
- `Sighting`: an instance of a researcher spotting a monster at a specific time and location
- `Researcher`: the human credited with finding the monster (unique across all sightings)
- `Monster`: the monster spotted (unique across all sightings)

To test the app's functionality, sample data is provided in the `sample` folder.

### Installation

Note the python version for the project is 2.7, and this is saved in the `.python-version` file in the project root directory.
1. Create a project directory called `squatch_watch` and `cd` in to it
2. Copy the `project.zip` file into `squatch_watch` and unzip it
3. Create another directory in `squatch_watch` for dependencies by running `virtualenv venv`
4. Activate the virtual environment with `source venv/bin/activate`
5. Install dependencies with `pip install -r requirements.txt`
6. Run the development server with `python manage.py runserver`
