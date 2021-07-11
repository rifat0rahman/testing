from Core.models import Reports, Reply
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
# for email
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    if request.method == 'POST':
       
       #try get the image file. sometime there might not be an image ,because its optional
        try:
            image = request.FILES['img_file']
        except:
            image = ''

        #here is a thing. I am using the title as 'name' field. this cacthes the data from the home page
        name = request.POST.get('title')
        email = request.POST.get('email')
        description = request.POST.get('des')

        # if everything ok,store that
        if description and name and email and image:
            report = Reports.objects.create(
                image=image, name=name, email=email, description=description)
            report.save()

        # if image is not present , that use the default one,(check in model.py image)
        if image == '':
            report = Reports.objects.create(name=name, email=email, description=description)
            report.save()

        #using this for send a notification to the original email from the dummy email.
        reportNotification(email,description)

        return redirect('success')

    
    return render(request, 'Home/home.html')

# succes page
def successIssue(request):
    return render(request, 'Home/success.html')



# only login who logged in
@login_required(login_url='/')
def reports(request):
    
    #get all the reports here
    reports = Reports.objects.all().order_by('-time')

    if request.method == 'POST':

        #trick to use two or more email host. usually you can't set that up in settings.py (you can,but it's hard)
        settings.EMAIL_HOST_USER = 'helpdesktorch@gmail.com'
        settings.EMAIL_HOST_PASSWORD = 'Hon37EY77!!'

        #taking the data for filtering otn- older to newer,you the rest.
        otn = request.POST.get('otn')
        nto = request.POST.get('nto')

        # this is from the pop up modal. it is the post request to send a reply email to the reporter
        report_id = request.POST.get('id')
        emailBody = request.POST.get('email-body')

        # checking the commands
        if otn:
            reports = Reports.objects.all().order_by('time')
        elif nto:
            reports = Reports.objects.all().order_by('-time')

        elif report_id and emailBody:
            user = Reports.objects.get(id=report_id)
            
            subject = f'clarifying the issue from Torch Help Desk on the subject of {user.name}'
            message = f'{emailBody}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)

            # using another function to store the data
            reply(message, user)
            return redirect('reports')

    context = {
        "reports": reports
    }

    return render(request, 'Reports/allreports.html', context)


# for deleting a report in the reports page
def delete_report(id):
    Reports.objects.get(id=id).delete()
    return redirect('reports')


#to create a database for storing all of the reply from the app
def reply(message, user):
    replies = Reply.objects.create(reporter_name=user.name,
                                   reporter_email=user.email,
                                   reply_body=message)
    replies.save()




# sending an email when a new report is created.
def reportNotification(email,description):
    
    # that's trick to use multiple email host.
    settings.EMAIL_HOST_USER = 'showtorchllc@gmail.com'
    settings.EMAIL_HOST_PASSWORD = 'Hon37ey77!'

    #there are some email stuff
    subject = f'A new report has been reported from Torch Help Desk'
    message = f'<issue> {description}. <reporter email> {email}'
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['helpdesktorch@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)
