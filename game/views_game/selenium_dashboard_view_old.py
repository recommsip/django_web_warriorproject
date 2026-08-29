from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import subprocess

  
 
# def selenium_dashboard(request):
#     print("Running login test.")
#     result = None
#     if request.method == "POST":
#         test = request.POST.get("test")
        
#         if test == "login":
#             # run login test
#             result = subprocess.run(["python", "game/testing/seltest_login.py"], capture_output=True, text=True)  
#             result = result.stdout.splitlines()
#             pass
        
#         elif test == "create_warrior":
#             # run create warrior test
#             result = subprocess.run(["python", "game/testing/seltest_create_warrior.py"], capture_output=True, text=True)  
#             result = result.stdout.splitlines()
#             pass
        
#         elif test == "seltest_03":
#             # run create warrior test
#             result = subprocess.run(["python", "game/testing/seltest_03.py"], capture_output=True, text=True)  
#             result = result.stdout.splitlines()
#             pass
        
    
#     return render(request,"selenium_testrunner/selenium_dashboard.html", {"result": result})


