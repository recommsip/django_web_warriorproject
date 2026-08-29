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

    def get(self, request, test_id):

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


    # def post(self,request):
        
    #     breakpoint()
    #     print("USER:", self.request.user)
    #     print("AUTHENTICATED:", self.request.user.is_authenticated)
    #     print("PERMISSIONS:")
    #     print(self.request.user.get_all_permissions())
        
    #     result = None

    #     tests = {
    #         "login": "game/testing/seltest_login.py",
    #         "create_warrior": "game/testing/seltest_create_warrior.py",
    #         "seltest_03": "game/testing/seltest_03.py",
    #     }
        
    #     if request.method == "POST":

    #         test = request.POST.get("test")

    #         if test == "all":
    #             print(test)
    #             result = []

    #             for test_name, test_path in tests.items():

    #                 result.append(f"===== RUNNING {test_name} =====")

    #                 completed = subprocess.run(
    #                     ["python", test_path],
    #                     capture_output=True,
    #                     text=True
    #                 )

    #                 result.extend(completed.stdout.splitlines())

    #                 if completed.returncode != 0:
    #                     result.append(
    #                         f"===== {test_name} FAILED ====="
    #                     )
    #                     break

    #                 result.append(
    #                     f"===== {test_name} PASSED ====="
    #                 )

    #         elif test in tests:

    #             completed = subprocess.run(
    #                 ["python", tests[test]],
    #                 capture_output=True,
    #                 text=True
    #             )

    #             result = completed.stdout.splitlines()

    #     return render(
    #         request,
    #         "selenium_testrunner/selenium_dashboard.html",
    #         {"result": result}
    #     )
        
        
    def post(self, request):
        
        test_name = request.POST.get("test")

        test_id = str(uuid.uuid4())

        print("name :",test_name,"id: ", test_id)
        TEST_RUNS[test_id] = {
            "status": "running",
            "output": []
        }

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
   
           try:
   
               if test_name == "login":
                   # run login test
                   result = subprocess.run(["python", "game/testing/seltest_login.py"], capture_output=True, text=True)  
                   result = result.stdout.splitlines()
                   TEST_RUNS[test_id]["output"].extend(result)
   
               elif test_name == "create_warrior":
                   # run create warrior test
                   result = subprocess.run(["python", "game/testing/seltest_create_warrior.py"], capture_output=True, text=True)  
                   result = result.stdout.splitlines()
                   TEST_RUNS[test_id]["output"].extend(result)
       
               else:
                   raise ValueError(
                       f"Unknown test: {test_name}"
                   )
   
               TEST_RUNS[test_id]["output"].append(
                   "TEST PASSED"
               )
   
               TEST_RUNS[test_id]["status"] = "passed"
   
           except Exception as e:
   
               TEST_RUNS[test_id]["output"].append(
                   f"TEST FAILED: {e}"
               )
   
               TEST_RUNS[test_id]["status"] = "failed"