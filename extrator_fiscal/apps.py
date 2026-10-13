from django.apps import AppConfig
from django.db.models.signals import post_migrate

def seed_demo_users(sender=None, **kwargs):
    try:
        from django.contrib.auth.models import User
        users = [
            ('kayck', 'kayck@unirv.edu.br', 'unirv2026', True),
            ('kayckrenan', 'kayck@unirv.edu.br', 'unirv2026', True),
            ('felipelopesgoncalves', 'felipe@unirv.edu.br', 'unirv2026', True),
            ('felipe', 'felipe@unirv.edu.br', 'unirv2026', True),
            ('admin', 'admin@unirv.edu.br', 'admin123', True),
        ]
        for username, email, pwd, is_super in users:
            u, created = User.objects.get_or_create(username=username, defaults={'email': email})
            if created or not u.check_password(pwd):
                u.set_password(pwd)
                u.is_staff = is_super
                u.is_superuser = is_super
                u.save()
    except Exception:
        pass

class ExtratorFiscalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'extrator_fiscal'

    def ready(self):
        post_migrate.connect(seed_demo_users, sender=self)
