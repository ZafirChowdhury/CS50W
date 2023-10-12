import markdown
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "index" : True
    })


def entry(request, wiki):
    page = util.get_entry(wiki)
    if page:
        return render(request, "encyclopedia/entry.html", {
            "wiki_name" : wiki,
            "page" : markdown.markdown(page),
        })
    
    else:
        return HttpResponse("Page not found (404)")
    

def search(request):
    if request.method == "POST":
        q = str(request.POST.get("q"))
        entries = util.list_entries()
        

        if q in entries:
            return HttpResponseRedirect("/" + q)
        
        matching_sub_str = []
        for i in entries:
            if q in i:
                matching_sub_str.append(i)

        return render(request, "encyclopedia/index.html", {
        "entries": matching_sub_str,
    })

    return HttpResponse("Please search using the search box.")


def random_page(request):
    q = random.choice(util.list_entries())
    return HttpResponseRedirect("/" + q)


def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        if title in util.list_entries():
            return HttpResponse("Entry already exists")
        
        util.save_entry(title, content)
        return HttpResponseRedirect("/" + title)

    return render(request, "encyclopedia/new.html")


def edit(request, wiki):
   return render(request, "encyclopedia/edit.html",{
        "title" : wiki,
        "content" : util.get_entry(wiki)
    })


def edit_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        util.save_entry(title, content)
        return HttpResponseRedirect("/" + title)
