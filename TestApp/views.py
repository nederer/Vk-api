from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
TOKEN = '&access_token=c9f2fe78c9f2fe78c9f2fe7822c982cce1cc9f2c9f2fe789795682ecf6a9af075786a18'
API = 'https://api.vk.com/method/'


def get_first_name(text):
    text = text[text.find('first_name')+13 :]
    return text[: text.find('"')]


def get_last_name(text):
    text = text[text.find("last_name")+12 :]
    return text[: text.find('"')]


def get_images(text):
    text = text[text.find("photo_200")+12 :]
    return text[: text.find('"')]


@login_required(login_url='/test/register/')
def main_page(request):
    
    #user info
    username = request.user.username
    json_text = requests.get(API+'users.get?user_ids='+str(username)+str(TOKEN)+'&v=5.8').text

    user_id = json_text[json_text.find("id")+4 : json_text.find(",")]
    user_first_name = get_first_name(json_text)
    user_last_name = get_last_name(json_text)

    # friends info
    friends_json = requests.get(API+'friends.get?user_id='+str(user_id)+str(TOKEN)+'&order=random&count=5&v=5.8').text

    friends_ids = friends_json[friends_json.find("[")+1 : friends_json.find("]")]
    friends_ids = friends_ids.split(',')
    
    friends_fnames = []
    friends_lnames = []
    images = []

    for f_id in friends_ids:
        json_text = requests.get(API+'users.get?user_ids='+str(f_id)+str(TOKEN)+'&fields=photo_200&v=5.8').text

        friends_fnames.append(get_first_name(json_text))
        friends_lnames.append(get_last_name(json_text))
        images.append(get_images(json_text))


    return render(request, 'TestApp/main_page.html', {'first_name': user_first_name, 'last_name': user_last_name,
                                                      'friends_fnames': friends_fnames, 'friends_lnames': friends_lnames,
                                                      'ids': friends_ids, 'img': images})


def register(request):
    return render(request, 'TestApp/registration.html', {})
