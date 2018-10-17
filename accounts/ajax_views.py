from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

def activate_users(request):
    if request.method == "POST":
        ids = request.POST.getlist('ids[]')

        User = get_user_model()
        user_name_list = []

        for id in ids:
            user = get_object_or_404(User, pk=id)
            user.is_active = True
            user.save()
            user_name_list.append(user.name)

        message = "{} 활성화 성공".format(','.join(user_name_list))
        return JsonResponse({'message': message})
            
    return JsonResponse({'error': '{} is unsupported method'.format(request.method)})


def deactivate_users(request):
    if request.method == "POST":
        ids = request.POST.getlist('ids[]')

        User = get_user_model()
        user_name_list = []

        for id in ids:
            user = get_object_or_404(User, pk=id)
            user.is_active = False
            user.save()
            user_name_list.append(user.name)

        message = "{} 비활성화 성공".format(','.join(user_name_list))
        return JsonResponse({'message': message})
            
    return JsonResponse({'error': '{} is unsupported method'.format(request.method)})