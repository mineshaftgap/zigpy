"""Does #1814 decode our (unencrypted, SrcID-addressed) Hue Tap button frames?

The Taps are ``SecurityLevel.NoSecurity``, so no commissioning payload or key
is needed — we register the device directly and push each operational frame
through the manager, exactly as ``test_real_frames.py`` does for the encrypted
Busch-Jaeger 6716U.

See zigpy/zigpy#1814.
"""

from __future__ import annotations

from tests.zgp.fixtures.hue_tap import (
    HUE_TAP_BUTTON_FRAMES,
    HUE_TAP_DEVICE_ID,
    HUE_TAP_SOURCE_ID,
)
from zigpy.zgp.device import GPDevice
from zigpy.zgp.events import CommandReceived
from zigpy.zgp.manager import GreenPowerManager
from zigpy.zgp.types import GPDCommandID, SecurityLevel


# -- The headline question: are our command IDs known to #1814? --------------


def test_command_ids_are_known_to_1814() -> None:
    """Every Tap button maps to a defined ``GPDCommandID`` (raises if not)."""
    mapped = {f.command_id: GPDCommandID(f.command_id) for f in HUE_TAP_BUTTON_FRAMES}
    assert mapped == {
        0x22: GPDCommandID.Toggle,
        0x10: GPDCommandID.RecallScene0,
        0x11: GPDCommandID.RecallScene1,
        0x12: GPDCommandID.RecallScene2,
    }


# -- Operational dispatch: does each button fire an event? -------------------


def _paired_tap(manager: GreenPowerManager) -> GPDevice:
    """Register the Tap as if commissioning had just completed (no key)."""
    device = GPDevice(
        source_id=HUE_TAP_SOURCE_ID,
        device_id=HUE_TAP_DEVICE_ID,
        frame_counter=0,
    )
    # Unencrypted by default — this is the path #1814 hasn't tested.
    assert device.security_level == SecurityLevel.NoSecurity
    manager.add_device(device)
    return device


async def test_each_button_fires_command_event(manager, gp_events) -> None:
    """All four unencrypted button frames each produce a ``CommandReceived``."""
    _paired_tap(manager)

    for counter, frame in enumerate(HUE_TAP_BUTTON_FRAMES, start=1):
        await manager._dispatch_gp_command(
            source_id=HUE_TAP_SOURCE_ID,
            frame_counter=counter,  # strictly increasing -> all accepted
            command_id=frame.command_id,
            payload=b"",
        )

    commands = [e for _, e in gp_events if isinstance(e, CommandReceived)]
    assert len(commands) == len(HUE_TAP_BUTTON_FRAMES)
    assert [int(c.command_id) for c in commands] == [
        f.command_id for f in HUE_TAP_BUTTON_FRAMES
    ]
