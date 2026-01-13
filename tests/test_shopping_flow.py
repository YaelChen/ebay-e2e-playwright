import pytest
from core.shopping_service import ShoppingService
from playwright.sync_api import Page


class TestShoppingFlow:
    """
    Test Suite - Full Shopping Flow E2E Tests
    """
    
    @pytest.mark.e2e
    def test_guest_shopping_flow(self, page: Page, test_data):
        """
        Full Shopping Flow Test - Guest Mode, Search, Add to Cart, Assert
        
        Test Steps:
        1. Login as Guest
        2. Search for items under price
        3. Add items to cart
        4. Assert that total does not exceed budget
        """
        # get data fron JSON
        scenario = test_data["test_scenarios"][0]  # first scenario
        
        print(f"\n{'='*60}")
        print(f"TEST: {scenario['test_name']}")
        print(f"{'='*60}")
        
        # create Service
        service = ShoppingService(page)
        
        # Login as Guest
        service.login_as_guest()
        
        # Search items under price
        urls = service.search_items_by_name_under_price(
            query=scenario["search_term"],
            max_price=scenario["max_price"],
            limit=scenario["items_limit"]
        )
        
        # Assert we found items
        assert len(urls) > 0, f"No items found for '{scenario['search_term']}' under ${scenario['max_price']}"
        
        print(f"\n✓ Found {len(urls)} items, proceeding to add to cart...")
        
        # Add items to cart
        service.add_items_to_cart(urls)
        
        # Assert cart total
        service.assert_cart_total_not_exceeds(
            budget_per_item=scenario["max_price"],
            items_count=len(urls)
        )
        
        print(f"\n{'='*60}")
        print(f"✓ TEST PASSED: {scenario['test_name']}")
        print(f"{'='*60}\n")
    
    
    @pytest.mark.e2e
    @pytest.mark.parametrize("scenario_index", [0, 1])
    def test_multiple_scenarios_data_driven(self, page: Page, test_data, scenario_index):
        """
        Data-Driven Test - runs on all scenarios in JSON
        @pytest.mark.parametrize - runs the test for each scenario index
        """
        scenario = test_data["test_scenarios"][scenario_index]
        
        print(f"\n{'='*60}")
        print(f"DATA-DRIVEN TEST: {scenario['test_name']}")
        print(f"{'='*60}")
        
        service = ShoppingService(page)
        
        # Login
        service.login_as_guest()
        
        # Search
        urls = service.search_items_by_name_under_price(
            query=scenario["search_term"],
            max_price=scenario["max_price"],
            limit=scenario["items_limit"]
        )
        
        assert len(urls) > 0, f"No items found"
        
        # Add to cart
        service.add_items_to_cart(urls)
        
        # Assert
        service.assert_cart_total_not_exceeds(
            budget_per_item=scenario["max_price"],
            items_count=len(urls)
        )
        
        print(f"\n✓ TEST PASSED")
    
    
    @pytest.mark.smoke
    def test_search_only(self, page: Page):
        """
        ⭐ Smoke Test - Search Only (Fast Check)
        """
        print(f"\n{'='*60}")
        print(f"SMOKE TEST: Search Only")
        print(f"{'='*60}")
        
        service = ShoppingService(page)
        service.login_as_guest()
        
        urls = service.search_items_by_name_under_price(
            query="laptop",
            max_price=500,
            limit=2
        )
        
        assert len(urls) > 0, "Search failed - no results"
        print(f"\n✓ SMOKE TEST PASSED: Found {len(urls)} items")