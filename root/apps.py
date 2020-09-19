from django.apps import AppConfig


class RootConfig(AppConfig):
    name = 'root'
     
    def ready(self):
        import root.signals
