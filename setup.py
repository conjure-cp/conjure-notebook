import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="conjure",
    version="v2.3.0",
    author="Ogabek Yusupov",
    author_email="ogabekyusupov@gmail.com",
    description="Conjure extension for jupyter notebook",
    long_description=long_description,
    url="https://github.com/conjure-cp/conjure-notebook",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
           'ipywidgets>=7,<8',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)