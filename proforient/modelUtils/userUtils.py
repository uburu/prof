from specialist.models import SpecialistProfile
from user.models import Profile
from modelUtils.emailSignInModel import EmailSignInUser

def userDefine(request):
    current_usr = EmailSignInUser()
    if SpecialistProfile.objects.filter(user__email=request.user).exists():
        current_usr = SpecialistProfile.objects.get(user_id=request.user.id)

    elif Profile.objects.filter(user__email=request.user).exists():
        current_usr = Profile.objects.get(user_id=request.user.id)
    return current_usr