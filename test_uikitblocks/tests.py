from json import dumps

from django.core.management.utils import get_random_secret_key
from django.test import TestCase
from .models import TestPage


# Create your tests here.
class TestUIKitBlocks(TestCase):

    def test_uikitblocks(self):
        test_page = TestPage(
            title="Test Page",
            slug="test-page",
            path="000100010001",
            depth=3,
            uikit_grid=dumps(
                [{"type": "UIKit", "value": {"container": "medium", "wrap_grid": None, "margin": [
                    {"type": "margin_top", "value": "medium", "id": "cc71a636-5dea-4edb-b0b5-2149f10b1468"}],
                                             "padding": [], "grid_blocks": [
                        {"background_color": "", "background_image": None, "uikit_block": [
                            {"type": "heading", "value": {"heading": "Hello World!", "color": "", "align": "center"},
                             "id": get_random_secret_key()}]}]},
                  "id": get_random_secret_key()}]
            ),
        )
        test_page.save()

        assert (
                '''<h1 class="uk-text-primary uk-text-center" style="">
    Hello World!
</h1>'''
                in test_page.uikit_grid.render_as_block()
        )
