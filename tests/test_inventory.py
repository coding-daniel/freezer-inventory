import os
import sys
import pytest

# Add src/ to the Python path so we can import from freezer_inventory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from freezer_inventory.main import InventoryManager

TEST_CSV = 'inventory/test_inventory.csv'

# Mocked version to override API call for predictability
class MockedInventoryManager(InventoryManager):
    def fetch_product_info(self, barcode):
        return f"MockProduct-{barcode}", "123 g"

@pytest.fixture
def manager():
    # Setup: create test manager and clean test CSV
    if os.path.exists(TEST_CSV):
        os.remove(TEST_CSV)
    manager = MockedInventoryManager(filename=TEST_CSV)
    yield manager
    # Teardown: clean test CSV
    if os.path.exists(TEST_CSV):
        os.remove(TEST_CSV)

def test_add_item_new(manager):
    item = manager.add_item("123456789", 3)
    assert item['quantity'] == 3
    assert item['name'] == "MockProduct-123456789"
    assert item['weight'] == "123 g"

def test_add_item_existing(manager):
    manager.add_item("123456789", 3)
    item = manager.add_item("123456789", 2)
    assert item['quantity'] == 5
    assert item['weight'] == "123 g"

def test_remove_quantity_partial(manager):
    manager.add_item("111", 5)
    item, message = manager.remove_quantity("111", 2)
    assert item['quantity'] == 3
    assert message == "Quantity updated."

def test_remove_quantity_all(manager):
    manager.add_item("222", 3)
    item, message = manager.remove_quantity("222", 3)
    assert item is None
    assert message == "Product removed completely."

def test_remove_product(manager):
    manager.add_item("333", 10)
    success = manager.remove_product("333")
    assert success is True
    assert "333" not in manager.inventory

def test_remove_nonexistent_product(manager):
    success = manager.remove_product("999")
    assert success is False

def test_add_item_manually_after_api_fail(manager):
    # Simulate a failed fetch
    class FailingMockedInventoryManager(InventoryManager):
        def fetch_product_info(self, barcode):
            return "Unknown product", "Unknown"

    test_manager = FailingMockedInventoryManager(filename=TEST_CSV)
    
    barcode = "0000000000000"
    quantity = 1

    # Add item (unknown returned, assume manual override)
    item = test_manager.add_item(barcode, quantity)
    item['name'] = "Manual Couscous"
    item['weight'] = "1 kg"
    test_manager.save_inventory()

    # Reload inventory to verify persistence
    test_manager = FailingMockedInventoryManager(filename=TEST_CSV)
    stored_item = test_manager.inventory[barcode]

    assert stored_item['name'] == "Manual Couscous"
    assert stored_item['weight'] == "1 kg"
    assert stored_item['quantity'] == 1

