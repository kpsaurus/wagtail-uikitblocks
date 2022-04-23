from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from uikitblocks import blocks as uikit_blocks


# Create your models here.
class TestPage(Page):
    uikit_grid = StreamField(
        [("UIKit", uikit_blocks.UIKitGrid())], blank=True, null=True
    )
