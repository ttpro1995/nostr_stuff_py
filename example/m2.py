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



message_pool = MessagePool(first_response_only=False)
policy = RelayPolicy()
io_loop = tornado.ioloop.IOLoop.current()
r = Relay(
    "wss://relay.damus.io",
    message_pool,
    io_loop,
    policy,
    timeout=2
)
# filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=100)])
filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE])])
subscription_id = uuid.uuid1().hex

r.add_subscription(subscription_id, filters)

try:
    io_loop.run_sync(r.connect)
except gen.Return:
    pass
io_loop.stop()

# while message_pool.has_notices():
#     print("notices")
#     notice_msg = message_pool.get_notice()
#     print(notice_msg.content)

flag = True
while flag:
    flag = False
    while message_pool.has_events():
        flag = True
        print("event")
        event_msg = message_pool.get_event()
        event_obj = event_msg.event
        simple_event = {
            "id": event_obj.id,
            "pubkey": event_obj.pubkey,
            "created_at": event_obj.created_at,
            "kind": event_obj.kind,
            # "tags": ",".join(event_obj.tags)
            "content": event_obj.content
        }
        # text = event_msg.event.content
        # print(json.dumps(event_obj, indent=4, cls=EventEncoder))
        print(json.dumps(simple_event))
    time.sleep(5)
