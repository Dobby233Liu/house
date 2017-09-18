# -*- coding: utf-8 -*-
import time
import random
import datetime

from disco.bot import Plugin, Config

EXPLATIVES = [
    'FUCKING',
    'GODDAMN',
    'MOTHERFUCKING',
    'PUNK ASS',
]

CHECK_MARK_EMOJI = u'\u2705'


def next_rotation(rotation, current):
    idx = rotation.index(current)
    if idx + 1 >= len(rotation):
        return rotation[0]
    return rotation[idx + 1]


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
    def load(self, ctx):
        super(TrashPlugin, self).load(ctx)

        self.trash = self.storage.plugin('trash')

        if 'next' not in self.trash:
            self.trash['next'] = self.config.rotation[0]

        if 'tuesday' not in self.trash:
            self.trash['tuesday'] = next_weekday(1)

        if 'wednesday' not in self.trash:
            self.trash['wednesday'] = next_weekday(2)

        self.spawn(self.remind_tuesday)
        self.spawn(self.remind_wednesday)

    def remind_until_acked(self, user):
        channel = self.state.channels.get(self.config.channel)
        msgs = []

        def _g():
            while True:
                if len(msgs):
                    msgs[-1].delete()

                msgs.append(channel.send_message(u'HEY {} ITS TIME TO TAKE OUT THE {} TRASH!!¡¡!!¡!¡!¡'.format(
                    user.mention,
                    random.choice(EXPLATIVES)
                )))

                msgs[-1].create_reaction(CHECK_MARK_EMOJI)

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

    def remind_tuesday(self):
        while True:
            self.trash['tuesday'] = next_weekday(1)
            time.sleep((self.trash['tuesday'] - datetime.datetime.now()).total_seconds())
            channel = self.state.channels.get(self.config.channel)
            channel.send_message("@here it's time to take your trash out to the bins!")

    def remind_wednesday(self):
        while True:
            self.trash['wednesday'] = next_weekday(2)
            who = self.trash['next']
            self.trash['next'] = next_rotation(self.config.rotation, who)

            time.sleep((self.trash['wednesday'] - datetime.datetime.now()).total_seconds())
            self.remind_until_acked(self.state.users.get(who))

    @Plugin.command('debug', group='trash')
    def trash_debug(self, event):
        event.msg.reply(u'Tuesday reminder @ `{}`\nWednesday reminder @ `{}`\nNext Up: `{}`'.format(
            self.trash['tuesday'],
            self.trash['wednesday'],
            str(self.state.users.get(self.trash['next'])),
        ))

    @Plugin.command('set', '<user:user>', group='trash')
    def trash_set(self, event, user):
        self.trash['next'] = user.id
        event.msg.reply(':ok_hand: looks like {} is the next sucka'.format(
            str(user)
        ))

    @Plugin.command('now', '[user:user]', group='trash')
    def trash_now(self, event, user=None):
        self.remind_until_acked(user or event.author)
