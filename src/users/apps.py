from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = 'src.users'
    verbose_name = _("Modulo de Usuarios")