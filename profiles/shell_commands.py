from django.contrib.auth import get_user_model

User = get_user_model()

random_ = User.objects.last()

# my followers
random_.profile.followers.all()

# who I follow
random_.is_following.all() # == random_.profile.following.all()

# En el template para saber a quien sigue el usuario conectado
#{{ request.user }} esta siguiendo a => {{ request.user.is_following.all }}

# Para saber en el template si sigo a un usuario o no
"""{% if user.profile in request.user.is_following.all %}
    Lo estoy siguiendo
{% endif %}"""
