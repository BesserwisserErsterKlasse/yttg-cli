from client import YttgClient
from env import env
from globalobjects.client.config import client_config

client: YttgClient = YttgClient(
    host=client_config.host,
    port=client_config.port,
    header_size=client_config.header_size,
    psk=env.crypto.pre_shared_secret,
)
