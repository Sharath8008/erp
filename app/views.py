from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .models import UploadedFile
import pandas as pd
import plotly.express as px
import os
import plotly.graph_objs as go
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def loginPage(request):
    page = 'login'
    # if request.user.is_authenticated:
    #     return redirect('home') takes from session

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'app/sign.html', context)

@never_cache
def logoutuser(request):
    logout(request)
    return redirect('login')

@never_cache
@login_required(login_url='login')
def home(request):
    uploaded_files = UploadedFile.objects.all()

    # Create a list to store parsed column names
    column_names = []

    # Loop through each UploadedFile instance
    for uploaded_file in uploaded_files:
        # Parse the JSON string and append column names to the list
        columns_json = uploaded_file.columns
        columns_list = json.loads(columns_json)
        column_names.extend(columns_list)

    # Remove duplicates and sort the list
    column_names = sorted(list(set(column_names)))

    context = {'uploaded_files': uploaded_files, 'column_names': column_names}
    return render(request, "app/dashboard.html", context)

@never_cache
def upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        file = request.FILES.get('file')

        if not file:
            return HttpResponseBadRequest("No file uploaded")

        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension not in ['.xls', '.xlsx']:
            return HttpResponseBadRequest("Invalid file format. Please upload an Excel file.")

        # Read the uploaded Excel file to get column names
        df = pd.read_excel(file)
        column_names = list(df.columns)

        # Save the column names as JSON
        columns_json = json.dumps(column_names)

        uploaded_file = UploadedFile(file=file, title=title, desc=desc, columns=columns_json)
        uploaded_file.save()

        # Redirect to the generate_chart view with the uploaded_file id
        return redirect('home')
    return render(request, 'app/dashboard.html')

@never_cache
def modify(request):
    if request.method == 'POST':
        uploaded_file_id = request.POST.get('uploaded_file')
        chart_type = request.POST.get('chart_type')
        x_axis_selected = request.POST.get('x_axis')
        y_axis_selected = request.POST.get('y_axis')

        try:
            # Retrieve the UploadedFile instance based on the selected ID
            uploaded_file = UploadedFile.objects.get(pk=uploaded_file_id)

            # Read the uploaded Excel file
            df = pd.read_excel(uploaded_file.file.path)

            # Retrieve and parse the JSON column names
            column_names = json.loads(uploaded_file.columns)

            # Generate the chart based on the selected chart type and axes
            if chart_type == "scatter":
                fig = px.scatter(df, x=x_axis_selected, y=y_axis_selected, title='Uploaded Data')
            elif chart_type == "bar":
                fig = px.bar(df, x=x_axis_selected, y=y_axis_selected, title='Uploaded Data')
            elif chart_type == "pie":
                fig = px.pie(df, names=x_axis_selected, title='Uploaded Data')
            elif chart_type == "table":
                fig = go.Figure(data=[go.Table(
                    header=dict(values=df[x_axis_selected].tolist()),
                    cells=dict(values=[df[y_axis_selected]])
                )])

                # Update the layout for better formatting if needed
                fig.update_layout(
                    title='Uploaded Data Table',
                    margin=dict(l=0, r=0, t=0, b=0)
                )

            chart = fig.to_html()

            # Debugging print statement
            print(x_axis_selected)


            uploaded_files = UploadedFile.objects.all()
            context = {"chart": chart, 'UploadedFile': uploaded_file, 'uploaded_files': uploaded_files, 'chart_type': chart_type, "column_names": column_names, 'x_axis_selected': x_axis_selected, 'y_axis_selected': y_axis_selected}
            return render(request, 'app/dashboard.html', context)


        except UploadedFile.DoesNotExist:
            return HttpResponseBadRequest("Invalid uploaded file ID")

    # Handle GET requests
    return render(request, 'app/dashboard.html')


def Inventory(request):
    return render(request, 'app/Inventory.html')

def hr(request):
    return render(request, 'app/hr.html')

def crm(request):
    return render(request, 'app/crm.html')

def fm(request):
    return render(request, 'app/fm.html')

def reports(request):
    return render(request, 'app/reports.html')

def scm(request):
    return render(request, 'app/scm.html')



def get_axes_options(request):
    if request.method == 'GET':
        uploaded_file_id = request.GET.get('uploaded_file_id')

        try:
            uploaded_file = UploadedFile.objects.get(pk=uploaded_file_id)
            column_names = json.loads(uploaded_file.columns)

            return JsonResponse({'x_axes': column_names, 'y_axes': column_names})

        except UploadedFile.DoesNotExist:
            return JsonResponse({'error': 'Invalid uploaded file ID'})



