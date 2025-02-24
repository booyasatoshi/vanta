from setuptools import setup, find_packages

setup(
    name="vanta-api-wrapper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="Virgil Vaduva",
    author_email="virgil@gmail.com",
    description="A Python wrapper for the Vanta API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/booyasatoshi/vanta",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)