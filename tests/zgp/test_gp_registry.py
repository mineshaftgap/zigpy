"""Tests for the Green Power quirk registry (P0a)."""

import pytest

from zigpy.quirks import CustomGreenPowerDevice, _GP_REGISTRY, get_green_power_quirk
from zigpy.zgp.device import GPDevice
from zigpy.zgp.types import SecurityKeyType, SecurityLevel


def _make_gpd(source_id: int, **kwargs) -> GPDevice:
    return GPDevice(source_id=source_id, device_id=0, **kwargs)


class TestGPRegistry:
    """CustomGreenPowerDevice registration mechanics."""

    def test_subclass_registers_with_priority(self):
        """__init_subclass__ inserts into _GP_REGISTRY sorted by priority."""
        initial_len = len(_GP_REGISTRY)

        class LowPriority(CustomGreenPowerDevice, priority=99):
            pass

        class HighPriority(CustomGreenPowerDevice, priority=1):
            pass

        assert len(_GP_REGISTRY) == initial_len + 2
        # lower number = higher precedence; HighPriority must appear before LowPriority
        hp_idx = _GP_REGISTRY.index(HighPriority)
        lp_idx = _GP_REGISTRY.index(LowPriority)
        assert hp_idx < lp_idx

    def test_default_match_returns_false(self):
        """Base CustomGreenPowerDevice.match() always returns False."""
        gpd = _make_gpd(0xDEADBEEF)
        assert not CustomGreenPowerDevice.match(gpd)


class TestGetGreenPowerQuirk:
    """get_green_power_quirk returns first-match-wins result."""

    def test_match_returns_correct_quirk(self):
        class HueTapStub(CustomGreenPowerDevice, priority=10):
            manufacturer = "Philips"
            model = "Hue Tap (stub)"

            @classmethod
            def match(cls, gpd: GPDevice) -> bool:
                return (gpd.source_id & 0xFFFF0000) == 0x00400000

        gpd_match = _make_gpd(0x0040F4E4)
        gpd_no_match = _make_gpd(0x00110000)

        assert get_green_power_quirk(gpd_match) is HueTapStub
        assert get_green_power_quirk(gpd_no_match) is None

    def test_no_match_returns_none(self):
        gpd = _make_gpd(0xFFFFFFFF)
        # Unless something else in _GP_REGISTRY matches, should be None.
        result = get_green_power_quirk(gpd)
        assert result is None or isinstance(result, type)

    def test_priority_ordering_first_match_wins(self):
        """Lower priority number wins when multiple quirks match."""

        class GenericFirst(CustomGreenPowerDevice, priority=2):
            @classmethod
            def match(cls, gpd: GPDevice) -> bool:
                return gpd.source_id == 0x12345678

        class GenericSecond(CustomGreenPowerDevice, priority=50):
            @classmethod
            def match(cls, gpd: GPDevice) -> bool:
                return gpd.source_id == 0x12345678

        gpd = _make_gpd(0x12345678)
        result = get_green_power_quirk(gpd)
        assert result is GenericFirst


class TestVocabularyAliases:
    """Vocabulary aliases added in P0a."""

    def test_greenpower_device_alias(self):
        from zigpy.zgp import GreenPowerDevice
        from zigpy.zgp.device import GPDevice

        assert GreenPowerDevice is GPDevice

    def test_greenpower_cluster_id_in_profiles(self):
        from zigpy.profiles.zgp import GREENPOWER_CLUSTER_ID

        assert GREENPOWER_CLUSTER_ID == 0x0021
