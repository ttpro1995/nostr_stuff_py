import json
import ssl
import time
from nostr.relay_manager import RelayManager

relay_manager = RelayManager()
# https://relayable.org/index.html
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relayable.org")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})  # NOTE: This disables ssl certificate verification
# relay_manager.open_connections({"cert_reqs": ssl.CERT_REQUIRED})  # NOTE: This disables ssl certificate verification
time.sleep(2)  # allow the connections to open

# while relay_manager.message_pool.has_notices():
#     notice_msg = relay_manager.message_pool.get_notice()
#     print(notice_msg.content)

x = relay_manager.message_pool.has_eose_notices()
print(x)
while relay_manager.message_pool.has_events():
    print("meow")
    event_msg = relay_manager.message_pool.get_event()
    print(event_msg.event.content)



relay_manager.close_connections()