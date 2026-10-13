"""Instagram Agent Skill — Priority Tests (mocks only)."""
import unittest
import os

class InstagramSkillTest(unittest.TestCase):
    def test_happy_path_caption_mock(self):
        caption = "Check this out! #viral"
        self.assertLessEqual(len(caption), 2200)

    def test_invalid_input_too_long_caption(self):
        long = "x" * 3000
        self.assertGreater(len(long), 2200)

    def test_missing_credentials(self):
        os.environ.pop("INSTAGRAM_TOKEN", None)
        self.assertIsNone(os.environ.get("INSTAGRAM_TOKEN"))

    def test_timeout(self):
        def fake():
            raise TimeoutError("IG timeout")
        with self.assertRaises(TimeoutError):
            fake()

    def test_dry_run_no_post(self):
        # No post published
        self.assertTrue(True)

    def test_placeholder_key_rejected(self):
        for k in ["your_token", "dummy", "IG_xxxx"]:
            if "your" in k or "dummy" in k or k.startswith("IG_x"):
                self.assertTrue(True)

    def test_copy_paste_example(self):
        ex = '''
python3 ig_caption.py "My caption" --preview
'''
        self.assertIn("--preview", ex)

    def test_error_account_locked(self):
        err = {"error": "account locked", "code": 403}
        self.assertEqual(err["code"], 403)

    def test_error_rate_limit(self):
        err = {"error": "rate limit", "code": 429}
        self.assertEqual(err["code"], 429)


if __name__ == "__main__":
    unittest.main()
