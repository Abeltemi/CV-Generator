from django.shortcuts import render
from .models import Profile

from django.http import HttpResponse
import pdfkit
from django.template import loader
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def cvForm(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('dob')
        summary = request.POST.get('summary')
        degree = request.POST.get('degree')
        school = request.POST.get('school')
        university = request.POST.get('university')
        previous_work = request.POST.get('previous_work')
        skills = request.POST.get('skills')
        
        profile = Profile(
            name=name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            summary=summary,
            degree=degree,
            school=school,
            university=university,
            previous_work=previous_work,
            skills=skills
        )
        
        profile.save()
        
        
    return render(request, 'pdf/cvform.html')

def resume(request, id):
    
    user_profile = Profile.objects.get(pk=id)
    
    #get the template using get_template()
    template = loader.get_template('pdf/resume.html')
    # render the template  using template.render(context)
    html = template.render({"user_profile":user_profile})
    # pass the html template to the pdfkit using from_string()
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8'
    }
    config = pdfkit.configuration(wkhtmltopdf=r'D:\newdir\wkhtmltox\bin\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html,False,options, configuration=config)
    # setting path
    
    
    # make sure you return a response using HttpResponse(pdf, content_type='app/pdf')
    response = HttpResponse(pdf, content_type='application/pdf')
    # set the response downloadable =>   response['Content-Disposition'] = 'attachment'
    response['Content-Disposition'] = 'attachment'
    
    # specify name of the file to be downloaded
    filename = "resume.pdf"
    return response