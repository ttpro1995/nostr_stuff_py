from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
import tornado.ioloop
from tornado import gen
import time
import uuid
import json
import os


class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        # Convert the Event object to a dictionary
        event_dict = {
            'pubkey': obj.pubkey,
            'content': obj.content,
            'created_at': obj.created_at,
            'kind': obj.kind,
            'tags': obj.tags,
            'id': obj.id,
            'sig': obj.sig
        }
        return event_dict


def get_datetime():
    from datetime import datetime
    current_datetime = datetime.now()

    # Format the datetime
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Print the formatted datetime
    return formatted_datetime


class SimpleEventEncoder(json.JSONEncoder):
    def default(self, obj):
        # Convert the Event object to a dictionary
        event_dict = {
            'pubkey': obj.pubkey,
            'content': obj.content,
            'created_at': obj.created_at,
            'kind': obj.kind,
            'id': obj.id,
            'sig': obj.sig
        }
        return event_dict


class NostrCrawler:
    def __init__(self):

        self.policy = RelayPolicy()
        self.relay_url = "wss://relayable.org"
        self.folder = "/data/nostr"
        io_loop = tornado.ioloop.IOLoop.current()

        # filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=100)])
        self.filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=400)])
        self.subscription_id = uuid.uuid1().hex

    def crawl_loop(self):
        message_pool = MessagePool(first_response_only=False)
        io_loop = tornado.ioloop.IOLoop.current()
        r = Relay(
            self.relay_url,
            message_pool,
            io_loop,
            self.policy,
            timeout=2
        )
        r.add_subscription(self.subscription_id, self.filters)
        try:
            io_loop.run_sync(r.connect)
        except gen.Return:
            pass
        io_loop.stop()

        file_name = os.path.join(self.folder, get_datetime() + ".jsonl")
        with open(file_name, "w") as f:
            while message_pool.has_events():
                event_msg = message_pool.get_event()
                event_obj = event_msg.event
                f.write(json.dumps(event_obj, cls=SimpleEventEncoder))
                f.write("\n")


if __name__ == "__main__":
    crawler = NostrCrawler()
    crawler.crawl_loop()