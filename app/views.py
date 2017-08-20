from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
import re


class HashCounter(object):

    def __init__(self,files=[]):
        self.hashtags = {}
        self.files= files

    def process_file(self,file_data, file_name):
        file_data.seek(0)
        for line in self.__read_lines_of_file(file_data):
            # each line can have multiple sentances.
            # split sentences into an array. also take questions and exclamations into consideration 
            try:
                sentences = re.split('[?!.][\s]*',line.decode('utf-8').lower())
            except AttributeError:
                sentences = re.split('[?!.][\s]*',line.lower())
                    
            for s in sentences:
                if s:
                    words = re.findall(r'\w+', s)
                    [self.__process_word(file_data, file_name, s, word) for word in words]

        return self.hashtags            

    def get_hashtags(self):
        for f in self.files:
            self.process_file(f.file, f.name)
            
        self.hashtags= sorted(self.hashtags.items(), key=lambda x: x[1]['count'], reverse=True)
        return self.hashtags

    def __read_lines_of_file(self, file):
        while True:
            data = file.readline()
            if not data:
                break
            yield data    

    def __process_word(self, file_data, file_name, sentence, word):
        if word in self.hashtags:
            hw = self.hashtags[word]
            self.hashtags.update({
                word: {
                    'count': hw['count'] +1,
                    'documents': hw['documents'] + [file_name] if not file_name in hw['documents'] else hw['documents'],
                    'sentences': hw['sentences'] + [sentence] if not sentence in hw['sentences'] else hw['sentences']
                }
            }) 
        else:
            self.hashtags[word]={
                'count' : 1,
                'documents' : [file_name],
                'sentences' : [sentence] 
            }        

class HashtagsIndex(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs): 
        files = request.FILES.getlist('hashfile')
        hash_counter= HashCounter(files)
        return render(request, 'hashtags.html', {'hashtags': hash_counter.get_hashtags()})