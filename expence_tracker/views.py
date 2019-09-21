from django.shortcuts import render
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from .models import History,db_login
	
his=""
summ=""
# Create your views here.
def loginfun(request):
	try:
		print(request.POST)
		if(request.POST.get("btn_login")!=None):
			if(User.objects.get(username=request.POST["username"])):
				q=User.objects.get(request.POST["username"])
				if(q.password==request.POST["password"]):
					print("Login Success")
					return render(request,"expence.html")
				else:
					return render(request,"login.html",{"msg":"Incorrect Password"})
			else:
				return render(request,"login.html",{"msg":"Incorrect User Name"})

		if(request.POST.get("btn_signin")!=None):
			if(User.objects.get(request.POST["uname"])):
				return render(request,"login.html",{"msg":"User Name Exists"})
			else:
				if(request.POST["pass"]==request.POST["conf_pass"]):
					q=User.objects.create_user(username=request.POST["uname"],password=request.POST["pass"])
					q.save()
				else:
					return render(request,"login.html",{"msg":"Password Doesn't Match"})
	except Exception as e:
		return render(request,"login.html",{"msg":"Something Went Wrong!"})
	return render(request,"login.html")
def expence(request):
	global tracker,his,summ
	History.objects.get_or_create(item="balance")
	summ=""
	his=""
	A_bal=History.objects.get(item="balance")
	bal=A_bal.price
	print(request.POST)
	try:

		if(request.POST.get("addbalance")!=None):
			q=History.objects.get(item="balance")
			q.price=int(q.price)+int(request.POST["amount"])
			q.save()
			history()
			bal=q.price
			return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ})

		if(request.POST.get("btndel")!=None):
			q=History.objects.get(id=request.POST["btndel"])
			q1=History.objects.get(item="balance")
			q1.price=int(q1.price)+q.price
			q1.save()
			q.delete()
			history()
			bal=q1.price
			return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ})

		if(request.POST.get("additem")!=None):
			a=request.POST["item"]
			b=request.POST['price']
			qq=History.objects.get(item="balance")
			if(int(qq.price)-int(b)<0):
				history()
				return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ,"errormsg":"You Have Insufficient Balance"})
			else:
				item=History.objects.create(item=a,price=b)
				item.save()
				qq.price=int(qq.price)-int(b)
				qq.save()
				bal=qq.price

		history()
		return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ})
	except Exception as e:
		print("error",e)
		history()
		return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ,"errormsg":"Enter Correct Cardinalities!"})

def summary():
	global summ
	itemsum=0
	print(summ,"hello")
	q=History.objects.all().values_list('item', flat=True).distinct()
	print(q)
	for i in q:
		print(i)
		if(i!="balance"):
			qq=History.objects.all()
			for j in qq:
				if(i.lower()==j.item.lower()):
					print(j.item,j.price)
					itemsum=itemsum+int(j.price)
			summ=summ+"<tr><td>"+i+"</td><td>"+str(itemsum)+"</td></tr>"
		print(itemsum)
		itemsum=0

def history():
	global his
	c=0
	summary()
	q=History.objects.all()
	for i in q:
		if(i.item!="balance"):
			his=his+"<tr><td>"+i.item+"</td><td>"+str(i.price)+"<button onclick='itemform_form.submit();' name='btndel' class='form-control btn-danger' value='"+str(i.id)+"' style='width: 100px;float: right;'>Delete</button></td></tr>"