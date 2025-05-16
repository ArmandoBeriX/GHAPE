

from django.urls import path
from .views import *

urlpatterns = [
    path('',principalView, name='#'),
    
    path('Selector/', selectorView, name='Selector'),
  
    path('Principal/', principalView, name='Principal')
   

]
