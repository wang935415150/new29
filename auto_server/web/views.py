from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from repository import models
from utils.page import Pagination
from web.seveice.server import ServerService
from django.views import View
import json
from django.utils.decorators import method_decorator
class Server_json(View):

    @method_decorator(requires_csrf_token)
    def dispatch(self, request, *args, **kwargs):
        self.server = ServerService(request)
        return super(Server_json, self).dispatch(request, *args, **kwargs,)

    def get(self,request):

        return self.server.fetch()


    def delete(self, request):
        return self.server.delete()

    def put(self,request):
        return self.server.save()

def server(request):
    return render(request,'server.html')

