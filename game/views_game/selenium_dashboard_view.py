from django.views import View
from django.shortcuts import render
import subprocess
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import threading
import uuid

from django.http import JsonResponse
from django.views import View


TEST_RUNS = {}
class SeleniumStatus(View):
    template_name = "game/selenium_status.html"
    """ en url selenium/status/<str:test_id> this view obtains a url parameter test_id. """
    def get(self, request, test_id):
        print(test_id)
        test = TEST_RUNS.get(test_id)

        if not test:
            return JsonResponse(
                {"error": "Test not found"},
                status=404
            )

        return JsonResponse(test)
class SeleniumTesting(LoginRequiredMixin, PermissionRequiredMixin, View):
    
    permission_required = 'game.view_seleniumtests'
    
    def get(self, request):

        print("USER:", request.user)
        print("AUTHENTICATED:", request.user.is_authenticated)
        print("PERMISSIONS:")
        print(request.user.get_all_permissions())

        return render(
            request,
            "selenium_testrunner/selenium_dashboard.html",
            {"result": None}
        )

def selenium_dashboard(request):
    """Display the Selenium test dashboard"""
    return render(request, 'selenium_testrunner/selenium_dashboard.html', {
        'result': []
    })