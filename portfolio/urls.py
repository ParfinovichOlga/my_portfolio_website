from django.urls import path
from .import views

urlpatterns = [
    path("", views.StartingPage.as_view(), name="home"),
    path("projects", views.AllProjects.as_view(), name="all_projects"),
    path("interesting", views.AddToInterestingView.as_view(), name="interesting"),
    path("delete/<id>", views.DeleteFromInteresting, name="remove_from_interesting"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("<tag>", views.SelectProjectsByTag.as_view(), name="get_by_tag"),
    path("category/<slug:slug>", views.CategoryProjectsView.as_view() , name="category_projects"),
    path("projects/<slug:slug>", views.ProjectDetailView.as_view(), name="project_detail"),
        
]