import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    "aiohttp",
    "asyncio",
    "tqdm"
]

setuptools.setup(
    name="async_requests",
    version="0.1.0",
    author="tforce7171",
    author_email="taiseimaruyama7171@gmail.com",
    description="asyncronus requests",
    url="https://github.com/tforce7171/async_requests.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=requires
)