from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name="pip-check-updates",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pcu = pip_check_updates.__main__:run",
        ]
    },
    include_package_data=True,
    package_data={},
    install_requires=requirements,
    setup_requires=["setuptools_scm", "pytest-runner"],
    use_scm_version=True,
    tests_require=["pytest"],
    test_suite="tests",
    author="Zeheng Li",
    author_email="imzehengl@gmail.com",
    maintainer="Zeheng Li",
    maintainer_email="imzehengl@gmail.com",
    description="A tool to upgrade dependencies to the latest versions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zehengl/pip-check-updates",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
