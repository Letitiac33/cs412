# File: models.py
# Author: Letitia Caspersen (letitiac@bu.edu), 3/22/2026
# Description: Model definition for Newton, MA voter data and CSV data loader

from django.db import models
import csv

def load_data():
    """Load voter records from CSV file into the database, replacing any existing records."""

    filename = '/Users/letitiacaspersen/Desktop/django/voter_analytics/newton_voters.csv'

    # Delete existing records to prevent duplicates
    Voter.objects.all().delete()

    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            Voter.objects.create(
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row['Residential Address - Apartment Number'],
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=row['Date of Birth'],
                date_of_registration=row['Date of Registration'],
                party_affiliation=row['Party Affiliation'],
                precinct_number=row['Precinct Number'],
                v20state=row['v20state'] == 'TRUE',
                v21town=row['v21town'] == 'TRUE',
                v21primary=row['v21primary'] == 'TRUE',
                v22general=row['v22general'] == 'TRUE',
                v23town=row['v23town'] == 'TRUE',
                voter_score=int(row['voter_score']),
            )

    print(f'Done. Loaded {Voter.objects.count()} voters.')

class Voter(models.Model):
    """Model to represent a registered voter in Newton, MA."""

    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.TextField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    # Election participation fields
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        """Return a string representation of this Voter."""
        return f'{self.first_name} {self.last_name}'
