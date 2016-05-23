"""vocabhelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import vocab.views as vocab

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', vocab.homepage),
    url(r'^vocabs/$', vocab.vocab_lists, name='vocab_lists'),
    url(r'^vocabs-(?P<show>\w+)/$', vocab.vocab_lists, name='vocab_lists_show'),
    url(r'^vocabs/submit/$', vocab.vocab_submit, name='vocab_submittal'),
    url(r'^vocabs/edit/(?P<vocab_id>\d+)/$', vocab.vocab_edit, name='vocab_edit'),
    url(r'^vocabs/(?P<chapter_id>\d+)/$', vocab.single_vocab_list, name='n_single_vocab_list'),
    url(r'^vocabs/(?P<chapter_id>\d+)-(?P<order>\w+)/$', vocab.single_vocab_list, name='a_single_vocab_list'),
    url(r'^vocabs/(?P<usb>\w+)/(?P<chapter_id>\d+)/$', vocab.single_vocab_list, name='n_single_vocab_list_usb'),
    url(r'^vocabs/(?P<usb>\w+)/(?P<chapter_id>\d+)-(?P<order>\w+)/$', vocab.single_vocab_list, name='a_single_vocab_list_usb'),
    url(r'^vocabs/multiselection/$', vocab.multiselection, name='vocab_multiselection'),
    url(r'^vocabs/multiselection-(?P<show>\w+)/$', vocab.multiselection, name='vocab_multiselection_usb'),
    url(r'^vocabs/multiview/$', vocab.multiview, name='vocab_multiview'),
    url(r'^vocabs/multiview-(?P<order>\w+)/$', vocab.multiview, name='vocab_multiview_o'),
    url(r'^fortress/$', vocab.fortress),
    url(r'^vocabs/dictation/$', vocab.dictation, name='dictation'),
]
