from django import forms

from .models import *

class CaseForm(forms.ModelForm):

	class Meta: 
		model = Case 
		fields = ('name', 'division', 'notes')

class CWCaseForm(forms.ModelForm):

	class Meta: 
		model = Case 
		fields = ('name', 'division', 'notes', 'status')	

class DirectorCaseForm(forms.ModelForm):

	class Meta: 
		model = Case 
		fields = ('name', 'caseworker', 'division', 'notes', 'status')	


class CommentForm(forms.ModelForm):

	class Meta: 
		model = Comment
		fields = ('title', 'body', 'document')
		# fields = ('title', 'body')