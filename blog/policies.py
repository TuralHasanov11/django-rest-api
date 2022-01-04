def canCreate(request):
    return True

def canUpdate(request, post):
    return request.user.is_admin or request.user == post.author

def canDelete(request, post):
    return request.user.is_admin or request.user == post.author
