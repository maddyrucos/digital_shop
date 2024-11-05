def userprofile(request):
    if request.user.is_authenticated:
        return {}
        #return {'user_profile': request.user.UserProfile}
    else:
        return {}
