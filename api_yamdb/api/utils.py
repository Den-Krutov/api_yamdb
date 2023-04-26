from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


def send_confirm_code(user):
    code = default_token_generator.make_token(user)
    send_mail(
        'Confim code',
        f'username: {user.username}, confirmation_code: {code}',
        'admin@yamdb.com',
        [user.email],
    )
