def notification_count(request):
    if request.user.is_authenticated:
        return {
            'notif_count': request.user.notifications.filter(is_read=False).count()
        }
    return {}