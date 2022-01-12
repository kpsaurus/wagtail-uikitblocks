import re
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from bs4 import BeautifulSoup
import urllib
from django.conf import settings


class Choices:
    MARGIN_CHOICES = (
        (None, "No Margin"),
        ("small", "Small Margin"),
        ("medium", "Medium Margin"),
        ("large", "Large Margin"),
    )

    PADDING_CHOICES = (
        (None, "No Padding"),
        ("small", "Small Padding"),
        ("medium", "Medium Padding"),
        ("large", "Large Padding"),
    )

    ANIMATION_CHOICES = (
        ("slide", "Slide"),
        ("fade", "Fade"),
        ("scale", "Scale"),
        ("pull", "Pull"),
        ("push", "Push"),
    )
    ALIGN_CHOICES = (
        ("left", "Left"),
        ("right", "Right"),
        ("center", "Center"),
        ("justify", "Justify"),
    )

    PRIORITY_CHOICES = (
        ("primary", "Primary"),
        ("secondary", "Secondary"),
        ("danger", "Danger"),
        ("muted", "Muted"),
    )

    CONTAINER_CHOICES = (
        ("large", "Large Width Container"),
        ("medium", "Medium Width Container"),
        ("small", "Small Width Container"),
    )

    GRID_CHILD_WIDTH_CHOICES = (
        (1, "1 Item"),
        (2, "2 Items"),
        (3, "3 Items"),
        (4, "4 Items"),
        (5, "5 Items"),
        (6, "6 Items"),
    )


"""
-------------------------------------------------------------------------------------------------------
                                                UIkit Component Blocks
------------------------------------------------------------------------------------------------------
"""


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        label="Image",
    )

    class Meta:
        template = "image.html"
        icon = "image"


class SlideshowBlock(blocks.StructBlock):
    animation = blocks.ChoiceBlock(
        choices=Choices.ANIMATION_CHOICES, required=False, default="slide"
    )
    auto_play = blocks.BooleanBlock(required=False)
    image_items = blocks.ListBlock(
        ImageBlock(),
        label="Slideshow",
    )

    class Meta:
        template = "slideshow.html"
        icon = "image"


class SliderBlock(blocks.StructBlock):
    gap = blocks.BooleanBlock(required=False, help_text="Gap between the images")
    center = blocks.BooleanBlock(
        required=False, help_text="Images will be aligned center to the element"
    )
    auto_play = blocks.BooleanBlock(required=False)
    number_of_images = blocks.ChoiceBlock(
        required=False,
        default=3,
        choices=Choices.GRID_CHILD_WIDTH_CHOICES,
        help_text="Number of images that will be displayed in the desktop mode",
    )
    image_items = blocks.ListBlock(
        ImageBlock(),
        label="Slider",
    )

    class Meta:
        template = "slider.html"
        icon = "image"


class Lightbox(blocks.StructBlock):
    animation = blocks.ChoiceBlock(
        choices=Choices.ANIMATION_CHOICES, required=False, default="slide"
    )
    number_of_images = blocks.ChoiceBlock(
        required=False,
        default=3,
        choices=Choices.GRID_CHILD_WIDTH_CHOICES,
        help_text="Number of images that will be displayed in the desktop mode",
    )
    image_items = blocks.ListBlock(
        ImageBlock(),
        label="Lightbox",
    )

    class Meta:
        template = "lightbox.html"
        icon = "image"


class HeadingBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    color = blocks.CharBlock(
        required=False, help_text="Preferred font color. Eg: red, #157b57..etc"
    )
    align = blocks.ChoiceBlock(
        choices=Choices.ALIGN_CHOICES, required=False, default="center"
    )

    class Meta:
        template = "heading.html"
        icon = "title"


class PopupBlock(blocks.StructBlock):
    button_text = blocks.CharBlock()
    popup_title = blocks.CharBlock()
    popup_message = blocks.RichTextBlock()

    class Meta:
        template = "popup.html"
        icon = "folder-open-1"


class SwitcherItem(blocks.StructBlock):
    switcher_title = blocks.CharBlock()
    switcher_body = blocks.TextBlock()


class SwitcherBlock(blocks.StructBlock):
    switcher_items = blocks.ListBlock(
        SwitcherItem(),
        label="Switcher",
    )

    class Meta:
        template = "switcher.html"
        icon = "list-ul"


class BannerBlock(blocks.StructBlock):
    banner_image = ImageChooserBlock(
        label="Image",
    )
    banner_title = blocks.CharBlock(required=True)
    banner_content = blocks.RichTextBlock(required=False)

    class Meta:
        template = "banner.html"
        icon = "image"


class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True)
    link = blocks.URLBlock(required=False)
    priority = blocks.ChoiceBlock(
        choices=Choices.PRIORITY_CHOICES, required=False, default="primary"
    )

    class Meta:
        template = "button.html"


class MarginBlock(blocks.StreamBlock):
    margin_top = blocks.ChoiceBlock(
        choices=Choices.MARGIN_CHOICES, required=False, default="no"
    )
    margin_bottom = blocks.ChoiceBlock(
        choices=Choices.MARGIN_CHOICES, required=False, default="no"
    )
    margin_left = blocks.ChoiceBlock(
        choices=Choices.MARGIN_CHOICES, required=False, default="no"
    )
    margin_right = blocks.ChoiceBlock(
        choices=Choices.MARGIN_CHOICES, required=False, default="no"
    )


class PaddingBlock(blocks.StreamBlock):
    padding_top = blocks.ChoiceBlock(
        choices=Choices.PADDING_CHOICES, required=False, default="no"
    )
    padding_bottom = blocks.ChoiceBlock(
        choices=Choices.PADDING_CHOICES, required=False, default="no"
    )
    padding_left = blocks.ChoiceBlock(
        choices=Choices.PADDING_CHOICES, required=False, default="no"
    )
    padding_right = blocks.ChoiceBlock(
        choices=Choices.PADDING_CHOICES, required=False, default="no"
    )


class LinkBlock(blocks.StructBlock):
    url = blocks.URLBlock(required=True)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        title = None
        desc = None
        image = None

        # With the help of beautiful soup, scrap the url and check 
        # whether the link has any possible title, thumbnail or description.
        try:
            # Open the URL as Browser, not as python urllib
            page = urllib.request.Request(
                value["url"], headers={"User-Agent": "Mozilla/5.0"}
            )
            infile = urllib.request.urlopen(page).read()
            html = infile.decode("utf-8")

            if not isinstance(html, BeautifulSoup):
                doc = BeautifulSoup(html, "html.parser")
            else:
                doc = html

            ogs = doc.html.head.findAll(property=re.compile(r"^og"))
            data = {}
            for og in ogs:
                if og.has_attr("content"):
                    data[og["property"][3:]] = og["content"]

            for key, value in data.items():
                if key == "title":
                    title = value
                if key == "description":
                    desc = value
                if key == "image":
                    image = value

            context["title"] = title
            context["desc"] = desc
            context["image"] = image
        except Exception as e:
            pass

        return context

    class Meta:
        template = "link.html"


"""
-------------------------------------------------------------------------------------------------------
                                                Compound Blocks
------------------------------------------------------------------------------------------------------
"""


class UIKitBlocks(blocks.StreamBlock):
    heading = HeadingBlock()
    image = ImageBlock()
    slideshow = SlideshowBlock()
    slider = SliderBlock()
    lightbox = Lightbox()
    popup = PopupBlock(label="Popup Message")
    switcher = SwitcherBlock(label="Switcher")
    banner = BannerBlock(label="Banner")
    button = ButtonBlock()
    link = LinkBlock()


class GridItemBlock(blocks.StructBlock):
    background_color = blocks.CharBlock(
        required=False, help_text="Preferred font color. Eg: red, #157b57..etc"
    )
    background_image = ImageChooserBlock(label="Background Image", required=False)
    uikit_block = UIKitBlocks(label="Block", required=False)


class UIKitGrid(blocks.StructBlock):
    container = blocks.ChoiceBlock(
        choices=Choices.CONTAINER_CHOICES, required=False, default=None
    )
    wrap_grid = blocks.BooleanBlock(
        required=False,
        help_text="Do you want to wrap the grid block items inside a card?",
    )
    margin = MarginBlock(
        required=False, help_text="Add predefined margins for this item"
    )
    padding = PaddingBlock(
        required=False, help_text="Add predefined paddings for this item"
    )
    grid_blocks = blocks.ListBlock(GridItemBlock(), label="Grid Blocks")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        # Default grid children counts in different devices.
        grid_children_count_medium = 3
        grid_children_count_large = 4
        grid_children_count_extra_large = 4

        if hasattr(settings, "UIKIT_GRID_CHILDREN_COUNT_MEDIUM"):
            grid_children_count_medium = settings.UIKIT_GRID_CHILDREN_COUNT_MEDIUM
        if hasattr(settings, "UIKIT_GRID_CHILDREN_COUNT_LARGE"):
            grid_children_count_large = settings.UIKIT_GRID_CHILDREN_COUNT_LARGE
        if hasattr(settings, "UIKIT_GRID_CHILDREN_COUNT_EXTRA_LARGE"):
            grid_children_count_extra_large = (
                settings.UIKIT_GRID_CHILDREN_COUNT_EXTRA_LARGE
            )

        context["grid_children_count_medium"] = grid_children_count_medium
        context["grid_children_count_large"] = grid_children_count_large
        context["grid_children_count_extra_large"] = grid_children_count_extra_large
        return context

    class Meta:
        template = "grid.html"
        icon = "placeholder"
