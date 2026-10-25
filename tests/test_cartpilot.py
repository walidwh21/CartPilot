import unittest
from cartpilot import plan_basket, Profile
from cartpilot.parser import parse


class ParserTests(unittest.TestCase):
    def test_finds_items_and_budget(self):
        r = parse("I need rice and milk under Rs 1,200", ["rice", "milk", "eggs"])
        self.assertEqual(r.wanted, ["rice", "milk"])
        self.assertEqual(r.budget, 1200.0)

    def test_alias(self):
        r = parse("some PB please", ["peanut butter"])
        self.assertEqual(r.wanted, ["peanut butter"])


class EngineTests(unittest.TestCase):
    def test_avoid_tag_is_respected(self):
        res = plan_basket("peanut butter", Profile(avoid_tags={"nuts"}))
        self.assertEqual(res["picks"][0].product.brand, "Sunny")

    def test_distance_filter(self):
        res = plan_basket("bread", Profile(max_distance_km=3))
        self.assertEqual(res["picks"][0].product.store, "FreshMart")

    def test_budget_forces_cheaper_basket(self):
        q = "rice milk eggs peanut butter"
        loose = plan_basket(q, Profile())
        tight = plan_basket(q, Profile(budget=loose["total"] - 20))  # cheapest feasible: swap to skim milk
        self.assertLess(tight["total"], loose["total"])
        self.assertTrue(tight["within_budget"])

    def test_impossible_budget_is_reported(self):
        res = plan_basket("rice milk eggs", Profile(budget=10))
        self.assertFalse(res["within_budget"])

    def test_unavailable_category(self):
        res = plan_basket("bread", Profile(avoid_tags={"gluten", "gluten-free"}))
        self.assertEqual(res["unavailable"], ["bread"])


if __name__ == "__main__":
    unittest.main()
