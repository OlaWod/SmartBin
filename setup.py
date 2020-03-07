import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SmartBin", # Replace with your own username
    version="0.0.1",
    author="OlaWod",
    author_email="756825440@qq.com",
    description="A smart rubbish bin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OlaWod/SmartBin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
