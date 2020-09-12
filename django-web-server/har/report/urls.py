
from django.contrib import admin
from django.urls import include, path

from har.report.views import (
    render_connection_view,
    render_report_creation_view,
    render_report_update_view,
    render_reports_view,
    render_report_deletion_view)

urlpatterns = [
    path('', render_connection_view),
    path('report/', render_report_creation_view),
    path('report/<int:id_>/', render_report_update_view),
    path('reports/', render_reports_view),
    path('report/<int:id_>/deletion', render_report_deletion_view)
]
