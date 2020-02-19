from django.db import models
from multiselectfield import MultiSelectField

LOCATION = (
	('l1', 'Andaman and Nicobar Islands'), ('l2', 'Andhra Pradesh'), ('l3', 'Arunachal Pradesh'), ('l4', 'Assam'), ('l5', 'Bihar'), ('l6', 'Chandigarh'), ('l7', 'Chhattisgarh'), ('l8', 'Dadra and Nagar Haveli and Daman and Diu'),
	('l9', 'Delhi'), ('l10', 'Goa'), ('l11', 'Gujarat'), ('l12', 'Haryana'), ('l13', 'Himachal Pradesh'), ('l14', 'Jammu and Kashmir'), ('l15', 'Jharkhand'), ('l16', 'Karnataka'), ('l17', 'Kerala'),
	('l18', 'Ladakh'), ('l19', 'Lakshadweep'), ('l20', 'Madhya Pradesh'), ('l21', 'Maharashtra'), ('l22', 'Manipur'), ('l23', 'Meghalaya'), ('l24', 'Mizoram'), ('l25', 'Nagaland'), ('l26', 'Odisha'),
	('l27', 'Puducherry'), ('l28', 'Punjab'), ('l29', 'Rajasthan'), ('l30', 'Sikkim'), ('l31', 'Tamil Nadu'), ('l32', 'Telangana'), ('l33', 'Tripura'), ('l34', 'Uttar Pradesh'), ('l35', 'Uttarakhand'), ('l36', 'West Bengal'),
)

STREAMS = (
	('engg', 'Engineering'),
	('mgmt', 'Management'),
	('med', 'Medical'),
	('law', 'Law'),
	('phrm', 'Pharmacy'),
	('hmgmt', 'Hotel Management'),
	('poly', 'Polytechnique'),
)

TIER = (
	('t1', 'Tier 1 - IITs, IIMs, and top institutes'),
	('t2', 'Tier 2 - Popular colleges'),
	('t3', 'Tier 3 - Local colleges and university'),
)

AVAILABLE_DATES = (
	('d1', 'This month'),
	('d2', '1-3 months ahead'),
	('d3', '3-6 months ahead'),
	('d4', '6 months >'),
)

GENDER_RATIO = (
	('r1', 'High female population'),
	('r2', 'High male population'),
	('r3', '1:1 or nearby'),
)

PURCHASING_POWER = (
	('p1', 'Very High'),
	('p2', 'High'),
	('p3', 'Medium'),
	('p4', 'Low'), 
)


class College(models.Model):
	location = models.CharField(max_length = 50, choices = LOCATION)
	total_students = models.IntegerField(default = 1)
	stream = MultiSelectField(choices = STREAMS, max_length = 30)
	tier = models.CharField(choices = TIER, max_length = 50)
	available_dates = MultiSelectField(choices = AVAILABLE_DATES, max_length = 30)
	gender_ratio = models.CharField(choices = GENDER_RATIO, max_length = 30)
	purchasing_power = models.CharField(choices = PURCHASING_POWER, max_length = 30)
	image = models.ImageField(upload_to='photos/', blank=True, null=True)
	name = models.CharField(max_length = 100)
	address = models.CharField(max_length = 200)

	def __str__(self):
		return str(self.name)

class User(models.Model):
	name = models.CharField(max_length=500)
	email = models.CharField(max_length=500)
	csrf_token = models.CharField(max_length=500)
	college = models.ForeignKey(College, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.name) + ", " + self.college.name