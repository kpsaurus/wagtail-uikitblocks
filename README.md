# Wagtail UIKit Blocks

A collection of <a target="_blank" href="https://getuikit.com">UIKit</a> components that can be used as a Wagtail StreamField block.

### Available UIKit components

- Container
- Grid
- Heading
- Image
- Slideshow
- Slider
- Lightbox
- Modal Popup
- Switcher
- Banner
- Button
- Link

Some components also have alignment, margin, padding, and animation properties as well.

## Quick start

- Install from PyPI

  ```
  pip install wagtail-uikitblocks
  ```

- Add "uikitblocks" to your INSTALLED_APPS
    ```
    INSTALLED_APPS = [
        ...
        'uikitblocks',
    ]
    ```
  
- In your models.py, import the uikitblocks module

  ```
  from uikitblocks import blocks
  ```
  
- The root component - which contains all the available components, is a grid (uk-grid) component, which can be used as a StreamField.

  ```  
  grid = StreamField(
        [("UIKit", blocks.UIKitGrid())], blank=True, null=True
    )
  ```
  
- Instead of adding the whole grid component, you can also add individual UIKit components to your model class as well. An example is given below.

  ```
    heading = StreamField(
    [("heading", blocks.HeadingBlock())], blank=True, null=True
    )
  ```


- Run ```python manage.py migrate``` to migrate the model changes.

- The UIKit library must be imported in order to display the changes. You can either do it manually (For more info, please see the UIKit's official documentation <a href="https://getuikit.com/docs/installation">here</a>) or you can load the production ready files via the template tag.

  Add the following in the base template.

  ```
  {% load uikit_assets %}
  ```

  Before closing the head tag, load css and js files by adding the following template tags.

  ```
  {% uikit_css %}
  {% uikit_js %}
  ```

  ## Optional configuration

  The number of children appear inside a grid can be altered.

  For example, if you want to display 4 children in extra large (above 1600px) screens, 3 children in large (above 1200px) screens, and 2 children in medium (above 960px) screens, add the following lines in your settings module. _Please note that only 1-6 are valid by default._

  ```
  UIKIT_GRID_CHILDREN_COUNT_EXTRA_LARGE = 4
  UIKIT_GRID_CHILDREN_COUNT_LARGE = 3
  UIKIT_GRID_CHILDREN_COUNT_MEDIUM = 2
  ```

  ## Demo

  ![](https://raw.githubusercontent.com/kpsaurus/wagtail-uikitblocks/main/demo.gif)