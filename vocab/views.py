from django.shortcuts import render
from .models import Chapter, Book, VocabListSubmitted
from .forms import VocabSubmittal
from django.http import HttpResponseRedirect, HttpResponse, Http404
import vocab.lcdcontroller as lcdcontroller
import threading

ALPHABETICAL = 'alphabetical'

def homepage(request):
    return render(request, 'homepage.html')

def vocab_lists(request, show = ''):
    ch = Chapter.objects.all()
    usb = VocabListSubmitted.objects.all()
    return render(request, 'vocab_lists.html', {'chapters' : ch, 'show' : show, 'usb' : usb, 'themecolor' : 'light-blue'})

def vocab_sort_alp(vo):
    pending_remove = []
    for i in vo:
        if '***' in i:
            pending_remove.append(i)
        elif i[0:2] == '**':
            index_of_i = vo.index(i)
            vo[index_of_i] = vo[index_of_i][2:]

    for i in pending_remove:
        vo.remove(i)

    acsii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    starting_letters = []
    for i in vo:
        if i[0] not in starting_letters and i[0] in acsii_letters:
            starting_letters.append(str(i[0]).capitalize()+'**')
    vo += starting_letters

    vo = list(set(vo))

    if '\r' in vo:
        vo.remove('\r')

    vo.sort(key=lambda y: y.lower())

    return vo

def single_vocab_list(request, chapter_id, order='original', usb=None):
    if usb:
        ch = VocabListSubmitted.objects.filter(id=chapter_id)[0]
        vo = ch.vocabs.split('\n')
        themecolor = 'teal'
    else:
        ch = Chapter.objects.filter(id=chapter_id)[0]
        vo = ch.vocabs.split('\n')
        themecolor = 'teal'
    if order == ALPHABETICAL:
        vo = vocab_sort_alp(vo)
    return render(request, 'single_vocab_lists.html', 
        {'chapter' : ch,
         'vocabs' : vo,
         'order' : order,
         'usb':usb, 
         'themecolor' : themecolor})

def multiselection(request, show = ''):
    ch = Chapter.objects.all()
    usb = VocabListSubmitted.objects.all()
    return render(request, 'vocab_list_selection.html', 
        {'chapters' : ch,  
        'usb':usb, 
        'show':show})

def multiview(request, order='original'):
    if not request.GET:
        return HttpResponseRedirect('/vocabs/multiselection')
    id_list = []
    usb_id_list = []
    for i in dict(request.GET):
        if request.GET[i] == 'on':
            if i[0:4] == 'usb_':
                usb_id_list.append(i[4:])
            else:
                id_list.append(i)
    vo = []
    chs = []
    usbs = []
    for i in id_list:
        ch = Chapter.objects.filter(id=i)[0]
        chs.append(ch)
        vo += ch.vocabs.split('\n')
    for i in usb_id_list:
        usb = VocabListSubmitted.objects.filter(id=i)[0]
        usbs.append(usb)
        vo += usb.vocabs.split('\n')

    if order == ALPHABETICAL:
        vo = vocab_sort_alp(vo)

    current_arguments = request.GET.urlencode()

    return render(request, 'multi_vocab_view.html', 
        {'vocabs' : vo, 
        'chapters': chs, 
        'order' : order,
        'current_arguments':current_arguments, 
        'usbs' : usbs})

def vocab_submit(request):
    if request.method == 'POST':
        d = dict(request.POST)
        data = {'book':d['book'][0],
                'number':d['chapter_number'][0],
                'name':d['chapter_name'][0],
                'vocabs':d['vocabs'][0],
                'passcode':d['passcode'][0]}
        try:
            if not(data['book'] and data['number'] and data['name'] and data['vocabs'] and data['passcode']) \
                    or len(data['book']) > 20 or len(data['name']) > 50 or len(data['passcode']) > 16:
                raise
            VocabListSubmitted.objects.create(book = data['book'],
                                              number = int(data['number']),
                                              name = data['name'],
                                              vocabs= data['vocabs'],
                                              passcode = data['passcode'])
        except:
            return_args = {'error_messages' : [], 'edit' : False}
            return_args.update(data)
            if not(data['book'] and data['number'] and data['name'] and data['vocabs'] and data['passcode']):
                return_args['error_messages'].append('Please fill in all the fields')
            if len(data['book']) > 20 or len(data['name']) > 50:
                return_args['error_messages'].append('Be careful of the word limits.')
            if len(data['passcode']) > 16:
                return_args['error_messages'].append('Too long for password')
            try:
                int(data['number'])
            except:
                return_args['error_messages'].append('Chapter Number should be an integer!')
            return render(request, 'vocab_submittal.html', return_args)
        return HttpResponseRedirect('/vocabs-showusersubmit/')
    elif request.method == 'GET':
        return render(request, 'vocab_submittal.html', {'edit' : False})

def vocab_edit(request, vocab_id):
    if request.method == 'POST':
        d = dict(request.POST)
        data = {'book':d['book'][0],
                'number':d['chapter_number'][0],
                'name':d['chapter_name'][0],
                'vocabs':d['vocabs'][0],
                'passcode':d['passcode'][0]}
        vo = VocabListSubmitted.objects.filter(id = vocab_id)
        try:
            if not(data['book'] and data['number'] and data['name'] and data['vocabs'] and data['passcode']) \
                    or len(data['book']) > 20 or len(data['name']) > 50:
                raise
            if data['passcode'] != vo[0].passcode:
                raise
            vo.update(
                book = data['book'],
                number = int(data['number']),
                name = data['name'],
                vocabs= data['vocabs'],)
        except:
            return_args = {'error_messages' : [], 'id': vocab_id}
            return_args.update(data)
            if not(data['book'] and data['number'] and data['name'] and data['vocabs'] and data['passcode']):
                return_args['error_messages'].append('Please fill in all fields.')
            if len(data['book']) > 20 or len(data['name']) > 50:
                return_args['error_messages'].append('Be careful of the word limits.')
            if data['passcode'] != vo[0].passcode:
                return_args['error_messages'].append('Wrong passcode.')
            try:
                int(data['number'])
            except:
                return_args['error_messages'].append('Chapter Number should be an integer!')
            return render(request, 'vocab_edit.html', return_args)
        return HttpResponseRedirect('/vocabs/usb/'+str(vocab_id))
    elif request.method == 'GET':
        vo = VocabListSubmitted.objects.filter(id = vocab_id)[0]
        return render(request, 'vocab_edit.html',
                {'book':vo.book,
                'number':vo.number,
                'name':vo.name,
                'vocabs':vo.vocabs,
                'id':vocab_id,
                'edit': True,})

def fortress(request):
    from time import sleep
    def neko(time):
        sleep(time)
        print("Tread ended")

    t = threading.Thread(target=neko, args=(5,), name="nekopara")
    t.start()

    i = 0
    for a in threading.enumerate():
        if a.name == "nekopara":
            print("meow", i)
        i = i + 1

    return HttpResponse("Look at the console and see the magic happens!")

def dictation(request):
    vocabs = []
    for key in request.GET:
        if 'usb' in key:
            key = key.split('_')
            usb = VocabListSubmitted.objects.filter(id=int(key[1]))[0]
            query_vocabs = usb.vocabs.split("\n")
            vocabs += query_vocabs
        else:
            query_vocabs = Chapter.objects.filter(id=int(key))[0].vocabs.split('\n')
            vocabs += query_vocabs
    vocabs = list(set(vocabs))
    pending_remove = []
    for i in vocabs:
        if '***' in i:
            pending_remove.append(i)
        elif i[0:2] == '**':
            index_of_i = vocabs.index(i)
            vocabs[index_of_i] = vocabs[index_of_i][2:]
    for i in pending_remove:
        vocabs.remove(i)
    for i in vocabs:
        if i == '' or i == '\r':
            vocabs.remove(i)
    dictationlist = [x.split("//") for x in vocabs]

    for th in threading.enumerate():
        if th.name == "dictation":
            HttpResponse("Please stop all current dictations before starting a new dictation.")

    t = threading.Thread(target = lcdcontroller.main, args=(dictationlist), name="dictation")
    t.start()

    return HttpResponse("Dictation has started")