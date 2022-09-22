import hashlib
from rest_framework.authtoken.models import Token
from django.template.loader import render_to_string
from django.conf import settings


def gen_forgot_mail(request, user):
    """Generates the forgot password email"""
    return render_to_string(
        "authn/forgot-pass.html",
        context={
            "RESET_END": f"forgot/?token={hash_token(get_token(user))}&email={user.email}",
            "SITE_URL": settings.SITE_URL,
        },
    )


def hash_token(token):
    """Hashes the token"""
    return hashlib.sha256(token.encode()).hexdigest()


def get_token(user):
    """Refreshes the token"""
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


def verify_forgot_token(user, token):
    """Verifies the token"""
    return hash_token(get_token(user)) == token
