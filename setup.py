import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Conjure Notebook",
    version="v0.0.9",
    author="Ogabek Yusupov, Özgür Akgün, Chris Jefferson",
    author_email="ogabekyusupov@gmail.com, ozgur.akgun@st-andrews.ac.uk, caj21@st-andrews.ac.uk",
    description="A Jupyter notebook extension for the automated constraint modelling tool Conjure",
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
