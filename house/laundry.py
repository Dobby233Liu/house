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

   
    @Plugin.command('help')
    def help(self, event):
        
        
        
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
        

        content = humanize.naturaltime(datetime.fromtimestamp(status['when']))
        event.msg.reply('The {} will be done in {}.'.format(device, content))
