from django.shortcuts import render
from .models import History

tracker={"Available Balance":0}		
his=""
summ=""
# Create your views here.
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


			# qq=History.objects.get(id="1")
			# print(qq)
			# # for i in qq:
			# qq.price=20
			# qq.item="food"
			# qq.save()

			# qr=History.objects.filter(item="food")
			# for i in qr:
			# 	print("filter :",i.item,i.price)

			# q=History.objects.all()
			# for i in q:
			# 	print("all :",i.item)

			# h_list=History.objects.raw('select * FROM expence_tracker_history')
			# print("database",h_list)
			# for i in h_list:
			# 	print("value in db",i.id,i.item,i.price)



			# if(tracker.get(a)!=None):
			# 	tracker[a]=tracker[a]+b
			# 	tracker["Available Balance"]=tracker["Available Balance"]-b
			# 	if(tracker["Available Balance"]<0):
			# 		print("\n You have insufficient Balance!")
			# 		tracker["Available Balance"]=tracker["Available Balance"]+b
			# 		tracker[a]=tracker[a]-b
			# 		history()
			# 		save1()
			# 		return render(request,"expence.html",{"balance":tracker["Available Balance"],"history":his,"errormsg":"You have insufficient Balance!"})

			# else:
			# 	tracker[a]=b
			# 	tracker["Available Balance"]=tracker["Available Balance"]-b
			# 	if(tracker["Available Balance"]<0):
			# 		print("\n You have insufficient Balance!")
			# 		tracker["Available Balance"]=tracker["Available Balance"]+b
			# 		del tracker[a]
			# 		history()
			# 		save1()
			# 		return render(request,"expence.html",{"balance":tracker["Available Balance"],"history":his,"errormsg":"You have insufficient Balance!"})

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
				if(i==j.item):
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