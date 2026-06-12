import enum

from .crypto import (  # noqa: F401
    build_nonce,
    decrypt_payload,
    decrypt_security_key,
    encrypt_payload,
    encrypt_security_key,
)
from .device import GPDevice, GreenPowerDevice, ieee_to_source_id, source_id_to_ieee  # noqa: F401
from .frame import (  # noqa: F401
    GPChannelRequestPayload,
    GPCommissioningAppInfo,
    GPCommissioningExtendedOptions,
    GPCommissioningOptions,
    GPCommissioningPayload,
)
from .types import *  # noqa: F403, F401
from .types import (  # noqa: F401
    DEFAULT_GP_LINK_KEY,
    GP_CLUSTER_ID,
    GP_ENDPOINT,
    GP_GROUP_ID,
    SecurityKeyType,
    SecurityLevel,
)

# Note: GreenPowerManager is not imported here to avoid circular imports
# with zigpy.zcl.clusters.greenpower. Import it directly:
#   from zigpy.zgp.manager import GreenPowerManager

# Convenience aliases.
GreenPowerDeviceData = GPDevice  # noqa: F811
GPSecurityLevel = SecurityLevel  # noqa: F811
GPSecurityKeyType = SecurityKeyType  # noqa: F811


class GPDeviceType(enum.IntEnum):
    """Green Power Device Type IDs (Zigbee GP spec table A.3)."""

    SWITCH_1_STATE = 0x00
    SWITCH_2_STATE = 0x01
    SWITCH_ON_OFF = 0x02
    SWITCH_LEVEL_CONTROL = 0x03
    SIMPLE_SENSOR = 0x04
    SWITCH_1_STATE_ADVANCED = 0x05
    SWITCH_2_STATE_ADVANCED = 0x06
    COLOR_DIMMER_SWITCH = 0x10
    LIGHT_SENSOR = 0x11
    OCCUPANCY_SENSOR = 0x12
    DOOR_LOCK_CONTROLLER = 0x20
    TEMPERATURE_SENSOR = 0x30
    PRESSURE_SENSOR = 0x31
    FLOW_SENSOR = 0x32
    INDOOR_ENVIRONMENT_SENSOR = 0x33
    MANUFACTURER_SPECIFIC = 0xFE
    UNDEFINED = 0xFF

GREENPOWER_CLUSTER_ID = GP_CLUSTER_ID
