from django.shortcuts import render
import requests
from subprocess import run,PIPE
from djangoOutput.load_word_model import gen_don, load_doc, save_doc, generate_seq
from djangoOutput.load_pop_model import gen_song, load_doc, save_doc, generate_seq
from djangoOutput.load_rodya_model import gen_crime, load_doc, save_doc, generate_seq
from djangoOutput.load_scary_model import gen_scary_story, load_doc, save_doc, generate_seq
from djangoOutput.load_news_model import gen_news, load_doc, save_doc, generate_seq
from djangoOutput.load_yelp_model import gen_yelp_review, load_doc, save_doc, generate_seq
from djangoOutput.load_lovecraft_model import gen_lovecraft, load_doc, save_doc, generate_seq
from djangoOutput.load_troll_model import gen_tweet, load_doc, save_doc, generate_seq
from djangoOutput.load_caesar_model import gen_caesar, load_doc, save_doc, generate_seq

import sys
import os
import logging

logger = logging.getLogger(__name__)

def button(request):
    logger.debug("Entering button view")
    print("RUNNING BUTTON")
    logger.debug("Exiting button view")
    return render(request,'index.html')

def output(request):
    logger.debug("Entering output view")
    print("RUNNING OUTPUT")
    data=requests.get("https://regres.in/api/users")
    print(data.text)
    data=data.text
    logger.debug("Exiting output view")
    return render(request,'index.html',{'data':data})

def external(request):
    logger.debug("Entering external view")
    print('Running external')
    #out=run([sys.executable,'/home/corn-nuts/Desktop/WORD2VEC_SPECIAL_FOLDER/project-04-story-spinner/djangoOutput/djangoOutput/load_word_model.py'],shell=False,stdout=PIPE)
    #print(os.getcwd())
    #print(out.stdout)
    
    if (request.method == 'POST'):
        response = ""
        print(request)
        print(request.POST)
       
        params = request.POST.get("inputtext")
        if (request.POST.get("Don_Button")):            
            response = gen_don(params)
        elif (request.POST.get("Pop_Button")):
            response = gen_song(params)
        elif (request.POST.get("Raskolnikov_Button")):
            response = gen_crime(params)
        elif (request.POST.get("Scary_Button")):
            response = gen_scary_story(params)
        elif (request.POST.get("News_Button")):
            response = gen_news(params)
        elif (request.POST.get("Yelp_Button")):
            response = gen_yelp_review(params)
        elif (request.POST.get("Lovecraft_Button")):
            response = gen_lovecraft(params)
        elif (request.POST.get("Troll_Button")):
            response = gen_tweet(params)
        elif (request.POST.get("Caesar_Button")):
            response = gen_caesar(params)
        logger.debug("Successfully processed external view")
        return render(request,'index.html',{'data1':response})
    logger.debug("Exiting external view")
