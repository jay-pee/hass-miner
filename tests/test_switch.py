
import pytest
from unittest.mock import AsyncMock, MagicMock

from custom_components.miner.switch import MinerActiveSwitch
from custom_components.miner.coordinator import MinerCoordinator


@pytest.fixture
def mock_coordinator():
    """Fixture to mock MinerCoordinator."""
    coordinator = AsyncMock(spec=MinerCoordinator)
    coordinator.data = {
        "mac": "test_mac",
        "is_mining": True,
        "make": "test_make",
        "model": "test_model",
        "fw_ver": "test_fw_ver",
        "config": {},  # This is the key part: an empty dictionary
    }
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.title = "Test Miner"
    coordinator.miner = AsyncMock()
    coordinator.miner.supports_shutdown = True
    coordinator.miner.supports_power_modes = True
    return coordinator


@pytest.mark.asyncio
async def test_async_turn_off_attribute_error(mock_coordinator):
    """Test that async_turn_off raises AttributeError when config is empty dict."""
    switch = MinerActiveSwitch(coordinator=mock_coordinator)

    with pytest.raises(AttributeError) as excinfo:
        await switch.async_turn_off()

    assert "'dict' object has no attribute 'mining_mode'" in str(excinfo.value)


@pytest.mark.asyncio
async def test_async_turn_on_no_error(mock_coordinator):
    """Test that async_turn_on does not raise AttributeError when config is empty dict."""
    # For async_turn_on, we need to mock get_config to return a mock object
    # that has a mining_mode attribute, as the error is in async_turn_off
    # when accessing self.coordinator.data["config"].mining_mode
    mock_config = MagicMock()
    mock_config.mining_mode = "some_mode"
    mock_coordinator.miner.get_config.return_value = mock_config

    switch = MinerActiveSwitch(coordinator=mock_coordinator)

    # This should not raise an AttributeError
    await switch.async_turn_on()
    # You can add assertions here to check if other parts of async_turn_on
    # behaved as expected, e.g., if miner.resume_mining was called.
    mock_coordinator.miner.resume_mining.assert_called_once()
