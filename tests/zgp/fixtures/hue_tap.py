"""Green Power frames for the original Philips Hue Tap (GPD).

Device: herdsman model ``8718696743133`` / modelID ``"GreenPower_2"``.
SrcID-addressed GPD (``ApplicationID`` 0b000), ``SecurityLevel.NoSecurity`` —
unencrypted, carries no key, commissions by button-press.

Verified live on Zigbee2MQTT 2026-06-09: pressing the four buttons decodes to
``press_1``..``press_4`` = command IDs ``0x22`` / ``0x10`` / ``0x11`` / ``0x12``.

Unlike the encrypted Busch-Jaeger fixture, these frames are **constructed, not
captured**: Z2M does not log raw GP bytes, and because the device is
unencrypted an operational frame is fully determined by
``(source_id, frame_counter, command_id)`` with no MIC to reproduce.

See zigpy/zigpy#1814.

Pure data module — import the constants directly.
"""

from __future__ import annotations

from typing import NamedTuple

# One of our paired Taps ("DC 1433"). 4-byte Source ID, SrcID-addressed.
HUE_TAP_SOURCE_ID: int = 0x0040F4E4

# GPD DeviceID 0x02, inferred from herdsman modelID "GreenPower_2"
# (herdsman names GP devices "GreenPower_<deviceID>"). Stored only; the
# operational dispatch path does not depend on it.
HUE_TAP_DEVICE_ID: int = 0x02


class ButtonFrame(NamedTuple):
    """One operational button press."""

    label: str  # Z2M's decoded action
    command_id: int  # GP command ID on the wire


# Verified against zigbee-herdsman HUE_TAP_LOOKUP and the live Z2M decode.
HUE_TAP_BUTTON_FRAMES: list[ButtonFrame] = [
    ButtonFrame("press_1", 0x22),  # Toggle
    ButtonFrame("press_2", 0x10),  # RecallScene0
    ButtonFrame("press_3", 0x11),  # RecallScene1
    ButtonFrame("press_4", 0x12),  # RecallScene2
]
