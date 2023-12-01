from setuptools import find_packages, setup



setup(
    name="utils",
    version="0.0.9",
    description="This is a package that contains some utilits that may be needed in some of my services",
    package_dir={"":"src"},
    author="emperorsixpacks",
    author_email="andrewoluwatomiwo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Private :: Do Not Upload"
    ],

    install_requires = ["pydantic >= 1.10.12", "fastapi>=0.100.1"]
)
