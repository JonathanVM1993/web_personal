import requests

def get_user_session(request):

    first_name = request.session.get('first_name')
    email = request.session.get('email')
    img = request.session.get('img')
    linkedin = request.session.get('linkedin')

    return {'first_name': first_name, 'user_email': email, 'user_img': img, 'user_linkedin': linkedin}

