from django.views import View
from collections import Counter
from django.http import HttpResponse
from django.shortcuts import render

class HashCounter(View):

    def post(self, request, *args, **kwargs):
        c = Counter()
        files= request.FILES.getlist('hashfile')
        for f in files:
            f.file.seek(0)
            file_text= f.read()
            c.update(file_text.split())

        return render(request, 'hashtags.html', {'hashtags': c.most_common()})