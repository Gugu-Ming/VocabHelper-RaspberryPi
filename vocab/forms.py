from django import forms

class VocabSubmittal(forms.Form):
    book = forms.CharField(max_length=20, label='book')
    number = forms.IntegerField(label='chapter_number')
    name = forms.CharField(max_length=50,label='chapter_name')
    vocabs = forms.CharField(label='vocab', widget=forms.Textarea)