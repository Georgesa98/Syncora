from setuptools import setup, find_packages

setup(
    name="syncora",
    version="0.1",
    author="George Salebe",
    author_email="georgesalebe0@gmail.com",
    description="a cli tool for managing local dev environment with docker",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/georgesa98/syncora",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "loguru",
        "docker",
    ],
    entry_points={
        "console_scripts": [
            "syncora=cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    include_package_data=True,
)
