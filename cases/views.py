from django.http import HttpResponse
from django.template import loader
from .models import *
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import *
from django.utils import timezone
from datetime import datetime, timedelta
from send_mail import send_mail

def get_advocate():
	try: 
		advocate = CaseWorker.objects.filter(id=1)[0]
		return advocate
	except Exception: 
		adv_user = User(username="advocates", password="saorocks", email = "advocate@asuc.org")
		adv_user.first_name = "Super"
		adv_user.last_name = "User"
		adv_user.save()
		adv_cw = CaseWorker(user=adv_user, bio="I am the Student Advocate", permissions="Student Advocate")
		adv_cw.save()
		return adv_cw

def get_caseworker_details(request):
	PERMISSION_CHOICES = (
		("General", "General"), 
		("Director", "Director"), 
		("Policy Coordinator", "Policy Coordinator"), 
		("Chief of Staff", "Chief of Staff"), 
		("Student Advocate", "Student Advocate"),
	)
	cw = CaseWorker.objects.filter(user = request.user)
	if len(cw) > 0: 
		return (cw[0], cw[0].permissions) 
	else: 
		return (None, None)


@login_required(login_url='/login/')
def index(request):
	cw_user, cw_permissions = get_caseworker_details(request)
	case_list = Case.objects.filter(user=request.user).order_by('-last_update')
	if cw_permissions == "General":
		case_list = Case.objects.filter(Q(user=request.user) | Q(caseworker=cw_user)).order_by('-last_update')
	elif cw_permissions == "Director" or cw_permissions == "Policy Coordinator":
		enddate = datetime.now()
		startdate = enddate - timedelta(days = 2)
		case_list = Case.objects.filter(Q(user=request.user) | Q(caseworker=cw_user) | Q(open_date__range=[startdate, enddate])).order_by('-last_update')
	elif cw_permissions == "Chief of Staff" or cw_permissions == "Student Advocate":
		case_list = Case.objects.all().order_by('-last_update')
	template = loader.get_template('cases/index.html')
	# open_list = case_list.filter(status='Open')
	# closed_list = case_list.filter(status='Closed')
	context = {
		# 'open_list': open_list,
		# 'closed_list': closed_list,
		'case_list': case_list,
	}
	return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def create(request): 
	if request.method == 'POST':
		print "checkpoint 1"
		form = CaseForm(request.POST, request.FILES)
		if form.is_valid(): 
			print ""
			advocate = get_advocate()
			case = form.save(commit=False)
			case.user = request.user 
			case.status = "Open"
			case.caseworker = advocate
			case.save()
			
			return redirect('case_detail', case.pk)

	else: 
		form = CaseForm()
	return render(request, 'cases/edit_case.html', {'form': form})

@login_required(login_url='/login/')
def edit(request, case_id): 
	'''
	(1) If student, can do generic edit, only on their own
	(2) If case worker, can change status and everything else, only if their own
	(3) If case worker, can change status and everything else, only if their own, ONLY WITHIN 24 HOURS
	(4) SA can do anything
	'''
	cw_user, cw_permissions = get_caseworker_details(request)
	case = get_object_or_404(Case, pk=case_id)
	if request.method == 'POST':
		form = CaseForm(request.POST, request.FILES, instance=case)
		if cw_permissions == "Director" or cw_permissions == "Policy Coordinator":
			form = CWCaseForm(request.POST, instance=case)
		elif cw_permissions == "Chief of Staff" or cw_permissions == "Student Advocate":
			form = DirectorCaseForm(request.POST, instance=case)
		if form.is_valid(): 
			case = form.save(commit=False)
			# case.user = request.user 
			# case.status = "Open"
			case.last_update = timezone.now()
			case.save()
			# email_message = "Your case has been updated. Please go to localhost:8000/cases" + str(case.id) + "/"
			# send_mail(case.user.email, case.name + " [Case Update]", email_message)

			# send_mail(case.caseworker.user.email, case.name + " [Case Update]", email_message)
			
			return redirect('case_detail', case.pk)

	else: 
		form = None
		prev_date = timezone.now() - timedelta(days = 2)
		
		if case.user == request.user:
			form = CaseForm(instance = case)
		elif (cw_permissions == "Chief of Staff" or cw_permissions == "Student Advocate") or ((cw_permissions == "Director" or cw_permissions == "Policy Coordinator") and (case.open_date > prev_date)):
			form = DirectorCaseForm(instance = case)
		elif case.caseworker == cw_user: 
			form = CWCaseForm(instance = case)
		else: 
			return HttpResponse("You do not have acccess to this case.")
		
	return render(request, 'cases/edit_case.html', {'form': form})


@login_required(login_url='/login/')
def results(request, case_id):
    response = "You're looking at the results of case %s."
    return HttpResponse(response % case_id)

@login_required(login_url='/login/')
def detail(request, case_id):
	try: 
		cw_user, cw_permissions = get_caseworker_details(request)
		case = Case.objects.get(pk=case_id)
		prev_date = timezone.now() - timedelta(days = 2)
		if (case.user == request.user or case.caseworker == cw_user or (cw_permissions == "Chief of Staff" or cw_permissions == "Student Advocate") or ((cw_permissions == "Director" or cw_permissions == "Policy Coordinator") and (case.open_date > prev_date) )) == False:
			return HttpResponse("You do not have acccess to this case.")
	except Case.DoesNotExist:
		raise Http404("Case does not exist")
	if request.method == 'POST':
		form = CommentForm(request.POST, request.FILES)
		if form.is_valid(): 
			comment = form.save(commit=False)
			comment.user = request.user 
			comment.case = case
			comment.created_date = timezone.now()
			comment.save()
			return redirect('case_detail', case.pk)

	else: 
		form = CommentForm()
	return render(request, 'cases/detail.html', {'case': case, 'form': form})

@login_required(login_url='/login/')
def update(request, case_id):
    response = "You're looking at the update of case %s."
    return HttpResponse(response % case_id)

@login_required(login_url='/login/')
def comment(request, case_id):
    response = "You're looking at the comment of case %s."
    return HttpResponse(response % case_id)

@login_required(login_url='/login/')
def delete(request, case_id):
	instance = Case.objects.get(id=case_id)
	instance.delete()
	return redirect('index')

