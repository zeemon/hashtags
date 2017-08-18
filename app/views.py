from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
import re

class HashCounter(View):

    def post(self, request, *args, **kwargs):
        self.hashtags = {}
        files= request.FILES.getlist('hashfile')
        
        for f in files:
            f.file.seek(0)
            for line in self.read_lines_of_file(f):
                # each line can have multiple sentances.
                # split sentences into an array. also take questions and exclamations into consideration 
                sentences = re.split('[?!.][\s]*',line.decode('utf-8').lower())
                for s in sentences:
                    if s:
                        words = re.findall(r'\w+', s)
                        [self.process_word(f, s, word) for word in words]

        self.hashtags= sorted(self.hashtags.items(), key=lambda x: x[1]['count'], reverse=True)
        return render(request, 'hashtags.html', {'hashtags': self.hashtags})

    def read_lines_of_file(self, file):
        while True:
            data = file.readline()
            if not data:
                break
            yield data    

    def process_word(self, file, sentence, word):
        if word in self.hashtags:
            hw = self.hashtags[word]
            self.hashtags.update({
                word: {
                    'count': hw['count'] +1,
                    'documents': hw['documents'] + [file.name] if not file.name in hw['documents'] else hw['documents'],
                    'sentences': hw['sentences'] + [sentence] if not sentence in hw['sentences'] else hw['sentences']
                }
            }) 
        else:
            self.hashtags[word]={
                'count' : 1,
                'documents' : [file.name],
                'sentences' : [sentence] 
            }        