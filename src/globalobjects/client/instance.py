from client import YttgClient
from globalobjects.client.config import client_config

client: YttgClient = YttgClient(
    host=client_config.host,
    port=client_config.port,
    header_size=client_config.header_size,
)
