import time
# import textwrap
import humanize

from datetime import datetime

from disco.bot import Plugin
from disco.types.message import MessageTable

DATA = {
    'washer': {
        'time': 20 * 60,
        'done': 'washed',
    },
    'dryer': {
        'time': 35 * 60,
        'done': 'dried',
    }
}


class LaundryPlugin(Plugin):
    def load(self, ctx):
        super(LaundryPlugin, self).load(ctx)
        self.data = {'washer': {}, 'dryer': {}}

    def enqueue(self, device):
        status = self.data.get(device)
        if not status:
            return

        delay = status['when'] - time.time()
        if delay <= 0:
            return

        time.sleep(delay)

        status = self.data.get(device)
        if not status:
            return

        status['channel'].send_message('Ok {}, your laundry is {}!'.format(status['user'].mention, DATA[device]['done']))

    @Plugin.command('help')
    def help(self, event):
        """
        Displays this message.
        """
        tbl = MessageTable()
        tbl.set_header('Command', 'Desc')

        for command in self.bot.commands:
            print command.get_docstring().strip()
            tbl.add(command.triggers[0], command.get_docstring().strip())

        event.msg.reply(tbl.compile())

    @Plugin.command('washer start', group='laundry', context={'device': 'washer'})
    @Plugin.command('dryer start', group='laundry', context={'device': 'dryer'})
    def start(self, event, device=None):
        """
        Indicates the {device} has been started with a new load.
        """
        status = self.data[device]

        if status:
            event.msg.reply(':warning: {} was already running, clearing previous status'.format(device))

        status['when'] = time.time() + DATA[device]['time']
        status['user'] = event.author
        status['channel'] = event.channel
        status['subs'] = []
        status['task'] = self.spawn(self.enqueue, device)
        event.msg.reply(':ok_hand: started {}'.format(device))

    @Plugin.command('washer done', group='laundry', context={'device': 'washer'})
    @Plugin.command('dryer done', group='laundry', context={'device': 'dryer'})
    def done(self, event, device=None):
        """
        Indicates the {device} has been emptied completely, and is ready for a new load.
        """
        status = self.data.get(device)
        if not status:
            event.msg.reply('The {} wasnt running!'.format(device))
            return

        if not status['task'].ready():
            status['task'].kill()

        extra = ''
        if status['subs']:
            nxt = status['subs'].pop()
            extra = ' Its your turn now {}'.format(nxt.mention)

        event.msg.reply(':ok_hand: {} is all ready to go.{}'.format(device, extra))

    @Plugin.command('washer need', group='laundry', context={'device': 'washer'})
    @Plugin.command('dryer need', group='laundry', context={'device': 'dryer'})
    def queue(self, event, device=None):
        """
        Adds you to the queue of people waiting to use the {device}.
        """
        status = self.data.get(device)
        if not status:
            event.msg.reply('The {} isn\'t being used by anyone yet!'.format(device))
            return

        self.data[device]['subs'].append(event.author)
        event.msg.reply(':ok_hand: you\'ve been added to the queue!')

    @Plugin.command('washer when', group='laundry', context={'device': 'washer'})
    @Plugin.command('dryer when', group='laundry', context={'device': 'dryer'})
    def when(self, event, device=None):
        """
        Displays when the {device} will be done.
        """
        status = self.data.get(device)
        if not status:
            event.msg.reply('The {} isn\t in use.'.format(device))
            return

        content = humanize.naturaltime(datetime.fromtimestamp(status['when']))
        event.msg.reply('The {} will be done in {}.'.format(device, content))
