from django import forms
from .models import Comment

class ContactForm(forms.Form):
    user_name = forms.CharField(label="Your name", max_length=50, error_messages={"required":"Please enter your name",})
    subject = forms.CharField(max_length=50)
    message = forms.CharField(label="Your message", widget=forms.Textarea)
    email = forms.EmailField(label="Your email", error_messages={"required":"Please enter your email. I'll get back to you!"})

class CommentForm(forms.ModelForm):    
    class Meta:
        model = Comment
        exclude = ["project"]
        labels = {
            "user_name": "Your name",
            "user_email": "Your email",
            "text": "Comment"
        }
        error_messages = {
            "user_name":{
                "required": "Your name must not be empty"},
            "user_email" :{
                "required": "Please enter your email"
            },
            "text":{
                "required": "Leave your comment"
            }  
        }
