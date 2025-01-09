from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.views import View
from .models import *
from .forms import ContactForm, CommentForm
from .tasks import send_email_task
from django.contrib import messages
from django.views.generic import ListView
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from .time_cache import timed_lru_cache



# Create your views here.

#Creates a pie chart with tools in use and keeps it in cache during 30 days, after this time updates the pie chart
@timed_lru_cache(days=30)
def create_pie():
    data = pd.DataFrame(columns=["tool","projects_count"])
    tags = Tag.objects.all()
    for i in range(len(tags)):
        data.loc[i+1] = [tags[i].caption, len(tags[i].projects.all())]
    fig = px.pie(
        labels=data.tool, 
        values=data.projects_count,          
        names=data.tool, 
        color_discrete_sequence=px.colors.sequential.Cividis
        )
    fig.update_traces(textposition="inside", textinfo="percent")
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig_div: str = plot(fig, output_type="div")      
    return fig_div


class StartingPage(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "portfolio/home.html", {"categories": categories, "form": ContactForm()})
    
    
    def post(self, request):
        form = ContactForm(request.POST) 
        #send email with celery asynchronous task       
        if form.is_valid():            
            message = f"Subject: {form.cleaned_data['subject']}\n{form.cleaned_data['user_name']} {form.cleaned_data['email']}\n{form.cleaned_data['message']}"            
            send_email_task.delay(message=message.encode('utf-8'))
            messages.success(request, "Your message was sent.Thank you for the email.\n I'll get back to you in a few days")
            return HttpResponseRedirect(reverse("home"))
    
        context = {
            "categories": Category.objects.all(),
            "form": form
        }
        return render(request, "portfolio/home.html", context)
         

#Get all projects by category
class CategoryProjectsView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        category_projects = category.projects.all().order_by("-date")         
        return render(request, "portfolio/categories.html", {"projects":category_projects, "category": category.name, "tag":None})
    

#Project details page
class ProjectDetailView(View):
    #Check if project in in session data
    def get_interesting(self, request, project_id):
        projects = request.session.get("interesting_projects")
        is_interesting = False
        if projects and project_id in projects:
            is_interesting = True
        return is_interesting

    def get(self, request, slug):
        required_project = get_object_or_404(Project, slug = slug)
        
        context = {
            "project":required_project,
            "tags": required_project.tags.all(),
            "comments": required_project.comments.all(), 
            "form": CommentForm(), 
            "is_interesting": self.get_interesting(request,required_project.id)
        }        
        return render(request, "portfolio/project-details.html", context)
    
    #Add a comment to the project
    def post(self,request, slug):
        form = CommentForm(request.POST)
        project = get_object_or_404(Project, slug=slug)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.save()
            messages.success(request, "You comment was added. Thank you!")
            return HttpResponseRedirect(reverse("project_detail", args=[slug]))
        context = {
            "project":project,
            "tags": project.tags.all(),
            "comments": project.comments.all(), 
            "form": form,
            "is_interesting": self.get_interesting(request, project.id)
        }        
        return render(request, "portfolio/project-details.html", context)
    


#Store project id in session
class AddToInterestingView(View):
    def get(self, request):
        interesting_projects_id = request.session.get("interesting_projects")
        context = {}
        context["has_projects"] = False        
        if interesting_projects_id:
            context["projects"] = Project.objects.filter(id__in=interesting_projects_id).order_by("-date")
            context["has_projects"] = True
        return render(request, "portfolio/interesting.html", context)    


    def post(self, request):
        intresting_projects = request.session.get("interesting_projects")

        if intresting_projects is None:
            intresting_projects = []

        project_id = int(request.POST["project_id"]) 

        if project_id not in intresting_projects:
            intresting_projects.append(project_id)
            request.session["interesting_projects"] = intresting_projects
            messages.success(request, "This project was added to interesting") 
        return HttpResponseRedirect(reverse("project_detail", args=[Project.objects.get(id=project_id).slug]) )
    

def DeleteFromInteresting(request, id):
    interesting_projects = request.session.get("interesting_projects")    
    request.session["interesting_progects"] = interesting_projects.remove(int(id))
    return HttpResponseRedirect(reverse ("interesting"))


#Get all projects by tag
class SelectProjectsByTag(View): 
    def post(self, request, tag):
        required_tag = Tag.objects.get(caption=tag)    
    
        context = {
            "projects":required_tag.projects.all().order_by("-date"),
            "tag": required_tag
        }
        return render(request, "portfolio/categories.html", context)
    

#Get all projects    
class AllProjects(ListView):
    model = Project
    template_name = "portfolio/categories.html"
    ordering = ["-date"]
    context_object_name = "projects"

#Page with personal information
class AboutView(View):
    def get(self, request):            
        context = {
            "pie": create_pie(),
            "cvs": CV.objects.all(),
            "courses": Course.objects.all(),
            "universityes": Education.objects.all(),
            "tools": Tag.objects.all().order_by("caption")
        }
        return render(request, "portfolio/about.html", context)

    #Download resume
    def post(self, request):
        cv = get_object_or_404(CV, id=request.POST["id"])       
        return FileResponse(cv.file.open(), as_attachment=True)

       
