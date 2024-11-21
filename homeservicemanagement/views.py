





def Home(request):
    user = ""
    error = ""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    ser1 = Service_Man.objects.all()
    ser = Service_Category.objects.all()
    for i in ser:
        count = 0
        for j in ser1:
            if i.category == j.service_name:
                count += 1
        i.total = count
        i.save()
    d = {'error': error, 'ser': ser}
    return render(request, 'home.html', d)


def contact(request):
    error = False
    if request.method == "POST":
        n = request.POST['name']
        e = request.POST['email']
        m = request.POST['message']
        status = Status.objects.get(status="unread")
        Contact.objects.create(status=status, name=n, email=e, message1=m)
        error = True
    d = {'error': error}
    return render(request, 'contact.html', d)
    
