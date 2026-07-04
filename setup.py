from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="area_calculator",
    version="0.3",
    author="Sergei Poluektov",
    author_email="seregatipich@outlook.com",
    description="Library for calculating the area of geometric shapes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seregatipich/area_calculator",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "sympy",
    ],
    extras_require={
        "dev": ["pytest", "hypothesis", "ruff", "isort"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
