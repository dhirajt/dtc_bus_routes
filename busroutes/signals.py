# -*- coding: utf-8 -*-
import json
import datetime
import firebase_admin

from django.db.models.signals import post_save
from django.dispatch import receiver

from firebase_admin import credentials, messaging

from busroutes.models import FirebaseNotification

firebase_admin.initialize_app()

@receiver(post_save, sender=FirebaseNotification, dispatch_uid="send_fcm_notification")
def send_fcm_notification(sender, instance, **kwargs):
    if instance.sent:
        return

    channel_id = instance.channel_id if instance.channel_id else None

    data = {}
    if instance.data:
        data['NotificationIntentType'] = instance.data.get('NotificationIntentType')
        data['URL'] = instance.data.get('URL')
        data['title'] = instance.data.get('title')
        data['body'] = instance.data.get('body')
        data['image_url'] = instance.data.get('image_url')

    notification = None
    android_notification = None
    if instance.notification and instance.notification.get('title') and instance.notification.get('body'):
        notification = messaging.Notification(
            title = instance.notification.get('title'),
            body = instance.notification.get('body'),
            image = instance.notification.get('image_url')
        )

        android_notification = messaging.AndroidNotification(
        	channel_id = channel_id
        )

    fcm_options = None
    if instance.fcm_options:
        fcm_options = messaging.FCMOptions(
            analytics_label=instance.fcm_options.get(
                'analytics_label', 'notif_' + datetime.datetime.now().strftime('%d%b%Y_%H%M%SPST'))
        )

    tokens = []
    if instance.tokens:
        tokens = instance.tokens

    response_id = ''
    if len(tokens) > 1:
        message = messaging.MulticastMessage(
            data = data,
            notification = notification,
            fcm_options = fcm_options,
            tokens = tokens,
            android=messaging.AndroidConfig(notification=android_notification)
        )
        messaging.send_multicast(message)
    elif len(tokens) == 1:
        message = messaging.Message(
            data = data,
            notification = notification,
            fcm_options = fcm_options,
            token = tokens[0],
            android=messaging.AndroidConfig(notification=android_notification)
        )
        response_id = messaging.send(message)
    else:
        message = messaging.Message(
            data = data,
            notification = notification,
            fcm_options = fcm_options,
            topic = 'NOTIFICATION_TOPIC',
            android=messaging.AndroidConfig(notification=android_notification)
        )
        response_id = messaging.send(message)
    instance.sent = True
    instance.save()
    