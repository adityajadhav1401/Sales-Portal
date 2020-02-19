from django.shortcuts import render,redirect
from .models import College, User
from django.views.static import serve
from django.template.defaulttags import register
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

NORTH_INDIA = ["Uttar Pradesh", "Uttarakhand", "Punjab", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Delhi", "Chandigarh"]
EAST_INDIA = ["Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Sikkim", "Tripura"]
WEST_INDIA = ["Goa", "Gujarat", "Maharashtra","Dadra and Nagar Haveli and Daman and Diu"]
SOUTH_INDIA = ["Andhra Pradesh", "Telangana", "Karnataka", "Kerala", "Tamil Nadu", "Puducherry", "Lakshadweep", "Andaman and Nicobar Islands"]

LOCATION = ["Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu",
	"Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala",
	"Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha",
	"Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]
STREAMS = ["Engineering", "Management", "Medical", "Law", "Pharmacy", "Hotel Management", "Polytechnique"]
TIER = ["Tier 1 - IITs, IIMs, and top institutes", "Tier 2 - Popular colleges", "Tier 3 - Local colleges and university"]
AVAILABLE_DATES = ["This month", "1-3 months ahead", "3-6 months ahead", "6 months >"]
GENDER_RATIO = ["High female population", "High male population", "1:1 or nearby"]
PURCHASING_POWER = ["Very High", "High", "Medium", "Low"]
TOTAL_STUDENTS = ["Below 1,000", "1,000 - 3,000", "3,000 - 5,000", "Above 5,000"]

LOCATION_DICT = {
	'Andaman and Nicobar Islands':'l1', 'Andhra Pradesh':'l2', 'Arunachal Pradesh': 'l3', 'Assam': 'l4', 'Bihar': 'l5', 'Chandigarh': 'l6', 'Chhattisgarh': 'l7', 'Dadra and Nagar Haveli and Daman and Diu': 'l8',
	'Delhi': 'l9', 'Goa': 'l10', 'Gujarat': 'l11', 'Haryana': 'l12', 'Himachal Pradesh': 'l13', 'Jammu and Kashmir': 'l14', 'Jharkhand': 'l15','Karnataka': 'l16', 'Kerala': 'l17',
	'Ladakh': 'l18', 'Lakshadweep': 'l19', 'Madhya Pradesh': 'l20', 'Maharashtra': 'l21', 'Manipur': 'l22', 'Meghalaya': 'l23', 'Mizoram': 'l24', 'Nagaland': 'l25', 'Odisha': 'l26',
	'Puducherry': 'l27', 'Punjab': 'l28', 'Rajasthan': 'l29', 'Sikkim': 'l30', 'Tamil Nadu': 'l31', 'Telangana': 'l32', 'Tripura': 'l33', 'Uttar Pradesh': 'l34', 'Uttarakhand': 'l35', 'West Bengal' : 'l36'}
STREAMS_DICT = {"Engineering" : "engg", "Management": "mgmt", "Medical": "med", "Law": "law", "Pharmacy": "phrm", "Hotel Management": "hmgmt", "Polytechnique": "ploy"}
TIER_DICT = {"Tier 1 - IITs, IIMs, and top institutes": "t1", "Tier 2 - Popular colleges": "t2", "Tier 3 - Local colleges and university": "t3"}
AVAILABLE_DATES_DICT = {"This month": "d1", "1-3 months ahead": "d2", "3-6 months ahead": "d3", "6 months >": "d4"}
GENDER_RATIO_DICT = {"High female population": "r1", "High male population": "r2", "1:1 or nearby": "r3"}
PURCHASING_POWER_DICT = {"Very High": "p1", "High": "p2", "Medium": "p3", "Low": "p4"}


LOCATION_FDICT = {
	'l1': 'Andaman and Nicobar Islands', 'l2': 'Andhra Pradesh', 'l3': 'Arunachal Pradesh', 'l4': 'Assam', 'l5': 'Bihar', 'l6': 'Chandigarh', 'l7' : 'Chhattisgarh', 'l8' : 'Dadra and Nagar Haveli and Daman and Diu',
	'l9' : 'Delhi', 'l10' : 'Goa', 'l11' : 'Gujarat', 'l12' : 'Haryana', 'l13' : 'Himachal Pradesh', 'l14':'Jammu and Kashmir', 'l15' : 'Jharkhand', 'l16' : 'Karnataka', 'l17': 'Kerala',
	'l18' : 'Ladakh', 'l19' : 'Lakshadweep', 'l20' :'Madhya Pradesh', 'l21' : 'Maharashtra', 'l22' : 'Manipur', 'l23' : 'Meghalaya', 'l24' : 'Mizoram', 'l25' : 'Nagaland', 'l26' : 'Odisha',
	'l27' : 'Puducherry', 'l28': 'Punjab', 'l29' : 'Rajasthan', 'l30' : 'Sikkim', 'l31' : 'Tamil Nadu', 'l32' : 'Telangana', 'l33': 'Tripura', 'l34' : 'Uttar Pradesh', 'l35' : 'Uttarakhand', 'l36' : 'West Bengal'}
TIER_FDICT = {
	't1': 'Tier 1 - IITs, IIMs, and top institutes',
	't2': 'Tier 2 - Popular colleges',
	't3': 'Tier 3 - Local colleges and university'}
GENDER_RATIO_FDICT = {
	'r1': 'High female population',
	'r2': 'High male population',
	'r3': '1:1 or nearby'}
PURCHASING_POWER_FDICT = {
	'p1': 'Very High',
	'p2': 'High',
	'p3': 'Medium',
	'p4': 'Low'}

# Create your views here.
@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)

@register.simple_tag(takes_context=True)
def url_replace(context, value, field):
	query = context['request'].GET.copy().urlencode()
	params = query.split('&')
	if (query == ""): params = []
	url = ""
	for param in params:
		val = param.split('=')
		if (val[0] == field):
			url += val[0] + '=' + str(value)
		else:
			url += val[0] + '=' + val[1]
		if (not param == params[-1]):
			url += '&'
	return url

def protected_serve(request,path,document_root=None,show_indexes=False):
	return serve(request,path,document_root,show_indexes)


def search_view(request):
	request.session.clear()
	return render(request, 'webpage/search.html', {})

def result_view(request):

	name = request.GET.getlist('name')
	email = request.GET.getlist('email')
	csrf_token = request.GET.getlist('csrfmiddlewaretoken')
	if (len(name) != 0):
		request.session['name'] = name[0]
		request.session['email'] = email[0]
		request.session['csrf_token'] = csrf_token[0]

	if (request.session.get('name') != None):
		name = request.session['name']
		email = request.session['email']
		csrf_token = request.session['csrf_token']
		session_type = 1
	else:
		name = ""
		email = ""
		csrf_token = ""
		session_type = 0

	budget = request.GET.getlist('budget')
	location = request.GET.getlist('location')
	total_students = request.GET.getlist('total_students')
	stream = request.GET.getlist('stream')
	tier = request.GET.getlist('tier')
	date = request.GET.getlist('date')
	ratio = request.GET.getlist('ratio')
	purchasing_power = request.GET.getlist('purchasing_power')
	sort_by = request.GET.getlist('sort_by')

	if ("Pan India" in location) or (len(location) == 0):
		filter_location = LOCATION
	else:
		filter_location = location
		if ("North India" in location):
			filter_location.remove("North India")
			filter_location.extend(NORTH_INDIA)
		if ("East India" in location):
			filter_location.remove("East India")
			filter_location.extend(EAST_INDIA)
		if ("West India" in location):
			filter_location.remove("West India")
			filter_location.extend(WEST_INDIA)
		if ("South India" in location):
			filter_location.remove("South India")
			filter_location.extend(SOUTH_INDIA)

	if ("Any" in stream) or (len(stream) == 0): filter_stream = STREAMS
	else: filter_stream = stream

	if ("Any" in tier) or (len(tier) == 0): filter_tier = TIER
	else: filter_tier = tier

	if ("Any" in date) or (len(date) == 0): filter_date = AVAILABLE_DATES
	else: filter_date = date

	if ("Any" in ratio) or (len(ratio) == 0): filter_ratio = GENDER_RATIO
	else: filter_ratio = ratio

	if ("Any" in purchasing_power) or (len(purchasing_power) == 0): filter_purchasing_power = PURCHASING_POWER
	else: filter_purchasing_power = purchasing_power

	# Single select query filter
	filter_location = [LOCATION_DICT[i] for i in filter_location]
	filter_stream = [STREAMS_DICT[i] for i in filter_stream]
	filter_tier = [TIER_DICT[i] for i in filter_tier]
	filter_ratio = [GENDER_RATIO_DICT[i] for i in filter_ratio]
	filter_date = [AVAILABLE_DATES_DICT[i] for i in filter_date]
	filter_purchasing_power = [PURCHASING_POWER_DICT[i] for i in filter_purchasing_power]

	results = College.objects.filter(location__in=filter_location, tier__in=filter_tier,
		gender_ratio__in=filter_ratio, purchasing_power__in=filter_purchasing_power)

	# Integer range select query filter
	if (len(total_students) == 0):
		results = results
	elif (total_students[0] == TOTAL_STUDENTS[0]):
		results = results.filter(total_students__lt=1000)
	elif (total_students[0] == TOTAL_STUDENTS[1]):
		results = results.filter(total_students__lt=3000)
		results = results.filter(total_students__gt=1000)
	elif (total_students[0] == TOTAL_STUDENTS[2]):
		results = results.filter(total_students__lt=5000)
		results = results.filter(total_students__gt=3000)
	elif (total_students[0] == TOTAL_STUDENTS[3]):
		results = results.filter(total_students__gt=5000)

	# Sort results
	if (len(sort_by) == 0): sort_by = 'Name'
	else: sort_by = sort_by[0]

	if (sort_by == 'Name') : results = results.order_by('name')
	elif (sort_by == 'Location') :
	    results = sorted(results, key=lambda n: (n.location[0], int(n.location[1:])))
	elif (sort_by == 'Students') : results = results.order_by('total_students')

	# Multi select query filter
	final_results = []
	for result in results:
		if ((sum([i in result.stream for i in filter_stream]) > 0) and
			(sum([i in result.available_dates for i in filter_date]) > 0)):
			final_results.append(result)

	page_number = request.GET.get('page', 1)
	paginator = Paginator(final_results, 10)
	try:
		page = paginator.page(page_number)
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	
	selected_list = []
	if (session_type):
		for entry in page:
			if len(User.objects.filter(name=name,email=email,csrf_token=csrf_token,college=entry))>0:
				selected_list.append(entry.pk)

	return render(request, 'webpage/results.html', {'name': name, 'email': email, 'session_type': session_type, 'sort_by' : sort_by, 'colleges': page, 'selected_list': selected_list, 'location_fdict' : LOCATION_FDICT, 'tier_fdict' : TIER_FDICT, 'gender_ratio_fdict' : GENDER_RATIO_FDICT, 'purchasing_power_fdict' : PURCHASING_POWER_FDICT})


@csrf_exempt
def add_college_view(request):
	if (request.session.get('name')!=None):
		name = request.session['name']
		email = request.session['email']
		csrf_token = request.session['csrf_token']
		college_pk = request.GET['college']
		college = College.objects.get(pk=college_pk)
		User.objects.create(name=name, email=email, csrf_token=csrf_token, college=college)
		return JsonResponse({'status': 200})
	else:
		return JsonResponse({'status': 404})

@csrf_exempt
def delete_college_view(request):
	if (request.session.get('name')!=None):
		name = request.session['name']
		email = request.session['email']
		csrf_token = request.session['csrf_token']
		college_pk = request.GET['college']
		college = College.objects.get(pk=college_pk)
		User.objects.filter(name=name, email=email, csrf_token=csrf_token, college=college).delete()
		return JsonResponse({'status': 200})
	else:
		return JsonResponse({'status': 404})


def get_college_view(request):
	if (request.session.get('name')!=None):
		name = request.session['name']
		email = request.session['email']
		csrf_token = request.session['csrf_token']
		colleges = User.objects.filter(name=name, email=email, csrf_token=csrf_token)
		total = str(len(colleges))
		return JsonResponse({'status': 200, 'colleges' : total})
	else:
		return JsonResponse({'status': 404})