from .base import *
import os

DEBUG = False

# En Render normalmente tienes una variable RENDER_EXTERNAL_HOSTNAME
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS = [render_host]
else:
    # Por si quieres probar en otro lado
    ALLOWED_HOSTS = ["*"]

# Clave secreta obligatoria en producción
SECRET_KEY = os.environ["SECRET_KEY"]  # lanza error si no está

# Si Render te da base de datos (Postgres), la configuras aquí.
# Ejemplo genérico si tuvieras DATABASE_URL:
# import dj_database_url
# DATABASES["default"] = dj_database_url.parse(os.environ["DATABASE_URL"])
