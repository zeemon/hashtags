from django.test import TestCase
import os
from .views import HashCounter


class HashtagCounterTestCase(TestCase):

	def setUp(self):
		module_dir = os.path.dirname(__file__)
		file_path = os.path.join(module_dir, "./test_files/doc1.txt")
		file = open(file_path)
		hash_counter= HashCounter()
		self.hashtags= hash_counter.process_file(file, 'doc1.txt')


	def test_occurrences_of_words(self):
		self.assertEquals (self.hashtags['the']['count'],119)
		self.assertEquals (self.hashtags['and']['count'],103)
		self.assertEquals (self.hashtags['people']['count'],13)


	def test_occurrences_of_word_in_sentences(self):
		self.assertEquals (len(self.hashtags['and']['sentences']), 63)