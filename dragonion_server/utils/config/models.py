from dataclasses import dataclass


@dataclass
class ConfigModel:
    ...


@dataclass
class ServiceModel:
    port: int
    client_auth_priv_key: str
    client_auth_pub_key: str

    service_id: str = None
    key_content: str = "ED25519-V3"
    key_type: str = "NEW"
