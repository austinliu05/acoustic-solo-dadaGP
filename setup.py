from setuptools import setup

PACKAGE_NAME = "asdadagp"

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version="0.1.0",
    author="Austin Liu, Ziyang Hu",
    author_email="",
    description="Modified dadaGP package (Sarmento et al., 2021) to handle acoustic fingerstyle tabs.",
    url="https://github.com/austinliu05/acoustic-solo-dadaGP",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
