from django.shortcuts import render
from .models import Chapter, Book, VocabListSubmitted
from .forms import VocabSubmittal
from django.http import HttpResponseRedirect, HttpResponse, Http404

ALPHABETICAL = 'alphabetical'

def homepage(request):
    return render(request, 'homepage.html')

def vocab_lists(request, show = ''):
    ch = Chapter.objects.all()
    usb = []
    if show == 'showusersubmit':
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
        themecolor = 'orange'
    if order == ALPHABETICAL:
        vo = vocab_sort_alp(vo)
    return render(request, 'single_vocab_lists.html', {'chapter' : ch, 'vocabs' : vo, 'order' : order,'usb':usb, 'themecolor' : themecolor})

def multiselection(request, show = ''):
    ch = Chapter.objects.all()
    usb = []
    if show == 'showusersubmit':
        usb = VocabListSubmitted.objects.all()
    return render(request, 'vocab_list_selection.html', {'chapters' : ch,  'usb':usb, 'show':show})

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

    return render(request, 'multi_vocab_view.html', {'vocabs' : vo, 'chapters': chs, 'order' : order,
                                                     'current_arguments':current_arguments, 'usbs' : usbs})

def vocab_submit(request):
    if request.method == 'POST':
        d = dict(request.POST)
        data = {'book':d['book'][0],
                'number':d['chapter_number'][0],
                'name':d['chapter_name'][0],
                'vocabs':d['vocabs'][0],}
        try:
            if data['book'] == '' or data['number'] == '' or data['name'] == '' or  data['vocabs'] == '' or len(data['book']) > 20 or len(data['name']) > 50:
                raise
            VocabListSubmitted.objects.create(book = data['book'],
                                              number = int(data['number']),
                                              name = data['name'],
                                              vocabs= data['vocabs'])
        except:
            return_args = {'error_messages' : [], 'edit' : False}
            return_args.update(data)
            if data['book'] == '' or data['number'] == '' or data['name'] == '' or  data['vocabs'] == '':
                return_args['error_messages'].append('None of the options should be blank!')
            if len(data['book']) > 20 or len(data['name']) > 50:
                return_args['error_messages'].append('Be careful of the word limit.')
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
                'vocabs':d['vocabs'][0],}
        vo = VocabListSubmitted.objects.filter(id = vocab_id)
        try:
            if data['book'] == '' or data['number'] == '' or data['name'] == '' or  data['vocabs'] == '' or len(data['book']) > 20 or len(data['name']) > 50:
                raise
            vo.update(book = data['book'],
                      number = int(data['number']),
                      name = data['name'],
                      vocabs= data['vocabs'])
        except:
            return_args = {'error_messages' : [], 'id': vocab_id}
            return_args.update(data)
            if data['book'] == '' or data['number'] == '' or data['name'] == '' or  data['vocabs'] == '':
                return_args['error_messages'].append('None of the options should be blank!')
            if len(data['book']) > 20 or len(data['name']) > 50:
                return_args['error_messages'].append('Be careful of the word limit.')
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