export DJANGO_SUPERUSER_EMAIL=admin@mail.com
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=password

pipenv run python /code/manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = '$DJANGO_SUPERUSER_USERNAME'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superusuario creado exitosamente.')
else:
    print('El superusuario ya existe, no se realizó ninguna acción.')
EOF