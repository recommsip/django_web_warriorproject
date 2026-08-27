from django.views import View
from django.shortcuts import render
import subprocess
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class SeleniumTesting(LoginRequiredMixin, PermissionRequiredMixin, View):
    
    permission_required = 'game.seleniumtests'
    
    def selenium_dashboard(self,request):
        
        breakpoint()
        print("USER:", self.request.user)
        print("AUTHENTICATED:", self.request.user.is_authenticated)
        print("PERMISSIONS:")
        print(self.request.user.get_all_permissions())
        
        result = None

        tests = {
            "login": "game/testing/seltest_login.py",
            "create_warrior": "game/testing/seltest_create_warrior.py",
            "seltest_03": "game/testing/seltest_03.py",
        }

        if request.method == "POST":

            test = request.POST.get("test")

            if test == "all":
                print(test)
                result = []

                for test_name, test_path in tests.items():

                    result.append(f"===== RUNNING {test_name} =====")

                    completed = subprocess.run(
                        ["python", test_path],
                        capture_output=True,
                        text=True
                    )

                    result.extend(completed.stdout.splitlines())

                    if completed.returncode != 0:
                        result.append(
                            f"===== {test_name} FAILED ====="
                        )
                        break

                    result.append(
                        f"===== {test_name} PASSED ====="
                    )

            elif test in tests:

                completed = subprocess.run(
                    ["python", tests[test]],
                    capture_output=True,
                    text=True
                )

                result = completed.stdout.splitlines()

        return render(
            request,
            "selenium_testrunner/selenium_dashboard.html",
            {"result": result}
        )