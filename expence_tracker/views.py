from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from .models import History
	
his=""
summ=""
loguser = None
bal=""
# Create your views here.
def loginfun(request):
	try:
		if(request.POST.get("btn_login")!=None):
			user=authenticate(username=request.POST["username"],password=request.POST["pass"])
			if(user!=None):
				login(request,user)
				print("Login Success")
				return redirect("expence")
			else:
				return render(request,"login.html",{"msg":"Incorrect User Name/Password"})

		if(request.POST.get("btn_signin")!=None):
			try:
				a=User.objects.get(username=request.POST["uname"])
				return render(request,"login.html",{"msg":"User Name Exists"})

			
			except:
				if(request.POST["pass"]==request.POST["conf_pass"]):
					q=User.objects.create_user(username=request.POST["uname"],password=request.POST["pass"],first_name=request.POST["fname"],last_name=request.POST["lname"])
					q.save()
				else:
					return render(request,"login.html",{"msg":"Password Doesn't Match"})
	except Exception as e:
		print("error :",e)
		return render(request,"login.html",{"msg":"Something Went Wrong!"})
	return render(request,"login.html")
	
def expence(request):
	global tracker,his,summ,loguser,bal
	History.objects.get_or_create(item="balance",uid=request.user.username)
	summ=""
	his=""
	A_bal=History.objects.get(item="balance",uid=request.user.username)
	bal=A_bal.price
	try:
		print(request.user.username)
		if (request.user.is_authenticated):
			loguser=request.user.first_name+" "+request.user.last_name
		else:
			return redirect("login")
		if(request.POST.get("logout")!=None):
			logout(request)
			return redirect("login")

		if(request.POST.get("addbalance")!=None):
			q=History.objects.get(item="balance",uid=request.user.username)
			q.price=int(q.price)+int(request.POST["amount"])
			q.save()
			history(request)
			bal=q.price
			lowbal(str(bal))
			return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ,"username":loguser})

		if(request.POST.get("btndel")!=None):
			q=History.objects.get(id=request.POST["btndel"])
			q1=History.objects.get(item="balance",uid=request.user.username)
			q1.price=int(q1.price)+q.price
			q1.save()
			q.delete()
			history(request)
			bal=q1.price
			lowbal(str(bal))
			return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ,"username":loguser})

		if(request.POST.get("additem")!=None):
			a=request.POST["item"]
			b=request.POST['price']
			qq=History.objects.get(item="balance",uid=request.user.username)
			if(int(qq.price)-int(b)<0):
				history(request)
				lowbal(str(bal))
				return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ,"errormsg":"You Have Insufficient Balance","username":loguser})
			else:
				item=History.objects.create(item=a,price=b,uid=request.user.username)
				item.save()
				qq.price=int(qq.price)-int(b)
				qq.save()
				bal=qq.price

		history(request)
		lowbal(str(bal))
		return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ,"username":loguser})
	except Exception as e:
		print("error",e)
		history(request)
		lowbal(str(bal))
		return render(request,"expence.html",{"balance":bal,"history":his,"summ":summ,"errormsg":"Enter Correct Cardinalities!","username":loguser})

def lowbal(request):
	global bal
	if(int(bal)<10):
		bal="<font color='red'>"+str(bal)+"</font>"
	elif(int(bal)<50):
		bal="<font color='orange'>"+str(bal)+"</font>"
	else:
		bal="<font color='lightgreen'>"+str(bal)+"</font>"
def summary(request):
	global summ
	itemsum=0
	q=History.objects.filter(uid=request.user.username).values_list('item'.lower(), flat=True).distinct()
	for i in q:
		if(i!="balance"):
			qq=History.objects.filter(uid=request.user.username)
			for j in qq:
				if(i.lower()==j.item.lower()):
					itemsum=itemsum+int(j.price)
			summ=summ+"<tr><td>"+i+"</td><td>"+str(itemsum)+"</td></tr>"
		itemsum=0

def history(request):
	global his
	c=0
	summary(request)
	q=History.objects.filter(uid=request.user.username).order_by('-id')
	for i in q:
		h=str(i.p_time.hour)+":"+str(i.p_time.minute)+":"+str(i.p_time.second)
		if(i.item!="balance"):
			his=his+"<tr><td>"+i.item+"</td><td>"+str(i.p_date)+"</td><td>"+str(h)+"</td><td>"+str(i.price)+"</td><td><button onclick='itemform_form.submit();' name='btndel' class='form-control btn-danger' value='"+str(i.id)+"' style='width: 100px;float: right;'>Delete</button></td></tr>"