from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import subprocess
import threading
import uuid


TEST_RUNS = {}


class SeleniumStatus(LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = 'game.view_seleniumtests'

    def get(self, request, test_id):
        print("TEST RUNS:", TEST_RUNS)
        print("STATUS REQUEST:", test_id)

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

        return render(
            request,
            "selenium_testrunner/selenium_dashboard.html",
            {"result": None}
        )

    def post(self, request):

        test_name = request.POST.get("test")

        print("TEST REQUESTED:", test_name)
        print("USER:", request.user)

        test_id = str(uuid.uuid4())

        TEST_RUNS[test_id] = {
            "status": "running",
            "output": []
        }
        print(test_id)
        thread = threading.Thread(
            target=execute_test,
            args=(test_id, test_name),
            daemon=True
        )

        thread.start()

        return JsonResponse({
            "test_id": test_id
        })


def execute_test(test_id, test_name):

    TEST_RUNS[test_id]["output"].append(
        "Starting Selenium..."
    )
    
    switch = {
        'case1': lambda: "this is case 1",
    }
    
    try:

        if test_name == "login":
            result = subprocess.run(
                ["python", "game/testing/seltest_login.py"],
                capture_output=True,
                text=True
            )

        elif test_name == "create_warrior":

            result = subprocess.run(
                ["python", "game/testing/seltest_create_warrior.py"],
                capture_output=True,
                text=True
            )
            
        elif test_name == "all":
        
                    result = subprocess.run(
                        ["python", "game/testing/seltest_login.py"],
                        capture_output=True,
                        text=True
                    )
        

        else:

            raise ValueError(
                f"Unknown test: {test_name}"
            )

        # Add Selenium output to our stored test output
        TEST_RUNS[test_id]["output"].extend(
            result.stdout.splitlines()
        )

        # Check whether Selenium succeeded
        if result.returncode == 0:

            TEST_RUNS[test_id]["output"].append(
                "TEST PASSED"
            )

            TEST_RUNS[test_id]["status"] = "passed"

        else:

            TEST_RUNS[test_id]["output"].append(
                "TEST FAILED"
            )

            TEST_RUNS[test_id]["status"] = "failed"

    except Exception as e:

        TEST_RUNS[test_id]["output"].append(
            f"TEST FAILED: {e}"
        )

        TEST_RUNS[test_id]["status"] = "failed"