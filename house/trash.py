# -*- coding: utf-8 -*-
import time
import random
import datetime

from disco.bot import Plugin, Config

EXPLATIVES = [
    'TemTemmie'
]







def next_weekday(weekday):
    d = datetime.datetime.now()

    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    obj = d + datetime.timedelta(days_ahead)

    obj = obj.replace(hour=20, minute=30, second=0)
    return obj


class TrashConfig(Config):
    channel = None
    rotation = []


@Plugin.with_config(TrashConfig)
class TrashPlugin(Plugin):
    
        self.trash = self.storage.plugin('trash')

        
        
    
        def _g():
            while True:
                
                msgs.append(channel.send_message(u'HEY {} ITS TIME TO TAKE OUT THE {} TRASH!!¡¡!!¡!¡!¡'.format(
                    user.mention,
                    random.choice(EXPLATIVES)
                )))

                

                # Wait 5 minutes
                time.sleep(300)

        thread = self.spawn(_g)

        while True:
            event = self.wait_for_event(
                'MessageReactionAdd',
                channel_id=channel.id,
                user_id=user.id).get()

            if event.message_id == msgs[-1].id:
                if event.emoji.name == CHECK_MARK_EMOJI:
                    thread.kill()
                    msgs[-1].delete()
                    channel.send_message(u'Ok, thank you for taking out the trash {}!'.format(user))
                    return

    
