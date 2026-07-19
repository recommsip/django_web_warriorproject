from django.views import View  # type: ignore[import]
from django.views.generic import ListView  # type: ignore[import]

class AnotherViewType(View):
    
    
    def another_view(self):
        print("This is a response request")