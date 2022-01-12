from setuptools import setup, find_packages
from os import path
from uikitblocks import __version__

DESCRIPTION = "Wagtail Streamblock"

root_dir = path.abspath(path.dirname(__file__))

with open(path.join(root_dir, "README.md")) as f:
    long_description = f.read()

setup(
    name="wagtail_uikitblocks",
    version=__version__,
    url="https://github.com/kpsaurus/wagtail-uikitblocks/",
    author="Krishna Prasad K",
    author_email="kp.pranavam@gmail.com",
    description="A collection of UIKit components that can be used as a Wagtail StreamField block.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Django>=3.0", "wagtail>=2.0"],
    keywords=[
        "python",
        "django",
        "wagtail",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Wagtail",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
