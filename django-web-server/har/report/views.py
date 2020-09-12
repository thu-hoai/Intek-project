from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render

from har.report.models import Report

from .forms import ReportForm, UserConnectionForm

# Create your views here.


def render_connection_view(request):
    """Handle connection page view"""
    if request.method == 'POST':
        # Generate form with data from the request
        form = UserConnectionForm(request.POST)
        # User Login handling
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f'Account login successfully for {user}')
            return redirect('/report')

        # User Register handling
        if form.is_valid():
            # Process data, insert into DB, generate
            user = form.save()
            # user = form.cleaned_data.get('username')
            login(request, user)
            messages.success(
                request, f'Account created successfully for {user.username}')
            # Redirect to report page it works
            return redirect('/report')

    else:
        # Redirect to report in case the user logined before
        if request.user.is_authenticated:
            return redirect("/report")
        # Get, generate blank form
        form = UserConnectionForm()

    return render(request, 'connection.html', {'form': form})


@login_required(login_url='/')
def render_report_creation_view(request):
    """Handle Report page view"""
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            # Update User
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect("/reports")

    else:
        form = ReportForm()
    return render(request, 'report_creation.html', {'form': ReportForm})


@login_required(login_url='/')
def render_report_update_view(request, id_):
    """Hanle Report Update View

    Args:
        request (WSGIRequest): A HttpRequest object
        id_ (int): identification of a report registered to the website

    Returns:
        A HttpResponse
    """
    # In case the report does not exists
    try:
        report = Report.objects.get(pk=id_)
    except Report.DoesNotExist:
        raise Http404("This report does not exist")

    # In case the report is not belong to the login user
    if request.user.username != report.user.username:
        raise PermissionDenied

    # Pass value to report form
    report_form = ReportForm(request.POST or None, instance=report)
    if report_form.is_valid():
        report_form.save()
        return redirect("/reports")
    return render(
        request, 'report_update.html', {'form': report_form})


@login_required(login_url='/')
def render_reports_view(request):
    """Handle Reports View

    Args:
        request (WSGIRequest): A HttpRequest object

    Returns:
        A HttpResponse
    """
    # Get all reports of the user and order descending by `update time`
    reports = Report.objects.filter(user=request.user).order_by('-update_time')
    return render(request, "reports.html", {"reports": reports})


@login_required(login_url='/')
def render_report_deletion_view(request, id_):
    """Hanle Report Deletion View

    Args:
        request (WSGIRequest): A HttpRequest object
        id_ (int): identification of a report registered to the website

    Returns:
        A HttpResponse
    """
    # Query and delete the selected id report
    Report.objects.filter(user=request.user).get(pk=id_).delete()
    return redirect('/reports')
