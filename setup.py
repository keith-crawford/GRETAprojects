import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="projectwilliamsville",
    version="0.0.1",
    author="ThinJetty Ltd.",
    author_email="info@thinjetty.com",
    description="Iternship Text Analysis Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://thinjetty.com",
    project_urls={
        "Web": "https://thinjetty.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10.12",
)