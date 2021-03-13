from django.shortcuts import render
from Forum.forms import contactformemail
from django.core.mail import send_mail

def contactsendmail(request):
    if request.method == "GET":
        form = contactformemail()
    else:
        form=contactformemail(request.POST)
        if form.is_valid():
            frommail = form.cleaned_data['frommail']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject,message,frommail,['spikecowboy123@gmail.com',frommail])
    return render(request, "contact.html", {'form':form})