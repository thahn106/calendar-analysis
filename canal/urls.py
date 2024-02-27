from django.urls import path
import canal.views


urlpatterns = [
    path("", canal.views.index, name="index"),
]
