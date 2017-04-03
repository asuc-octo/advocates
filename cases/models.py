from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from django.utils.deconstruct import deconstructible

# @deconstructible
class CaseWorker(models.Model):
	PERMISSION_CHOICES = (
		("General", "General"), 
		("Director", "Director"), 
		("Policy Coordinator", "Policy Coordinator"), 
		("Chief of Staff", "Chief of Staff"), 
		("Student Advocate", "Student Advocate"),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	permissions = models.CharField(max_length=200, choices=PERMISSION_CHOICES)
	def __str__(self):
		return str(self.user) + " | " + str(self.permissions)
	# @staticmethod
	# def get_default(cl):
	# 	return cl.objects.all()[0]



# advocate = CaseWorker.objects.all()[0]

class Case(models.Model): 
	DIVISION_CHOICES = (
		('Academic', (
				('Grade Appeals', 'Grade Appeals'), 
				('Enrollment', 'Enrollment'), 
				('Withdrawal', 'Withdrawal'), 
				('Unfair Testing', 'Unfair Testing'),
			)
		), 
		('Financial Aid', (
				('Financial Aid', 'Financial Aid'), 
				('Residency for Tuition', 'Residency for Tuition'), 
				('SHIP', 'SHIP'),
			)
			
		),
		('Conduct and Grievance', (
				('Drugs and Alcohol', 'Drugs and Alcohol'), 
				('Sexual Assault', 'Sexual Assault'), 
			)
		),
	)
	STATUS_CHOICES = (
		('Open', 'Open'),
		('Closed', 'Closed'),
	)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
	caseworker = models.ForeignKey(CaseWorker, on_delete=models.CASCADE, related_name="cw")
	status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Open')
	name = models.CharField(max_length=200)
	division = models.CharField(max_length=200, choices=DIVISION_CHOICES)
	# case_type = models.CharField(max_length=200, default='')
	open_date = models.DateTimeField('date created')
	last_update = models.DateTimeField('last update date')
	notes = models.TextField(max_length=2000)
	
	def days_open(self):
		if self.status == "Closed": 
			return abs((self.last_update - self.open_date).days)
		else: 
			return abs((timezone.now() - self.open_date).days)
	def __str__(self):
		return str(self.user) + " | " + str(self.caseworker) + " | " + self.name

class Comment(models.Model): 
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	case = models.ForeignKey(Case, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	body = models.TextField()
	created_date = models.DateTimeField('date comment created', default=timezone.now())
	def user_directory_path(instance, filename):
	    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	    return 'user_{0}/{1}'.format(instance.user.id, filename)

	document = models.FileField(upload_to=user_directory_path, null=True, blank=True)
	
	def __str__(self):
		return str(self.user) + " | " + self.title


