from pytz import timezone

from django.conf import settings


def tz_local(data):
    fuso_horario = timezone(settings.TIME_ZONE)
    return data.astimezone(fuso_horario)
