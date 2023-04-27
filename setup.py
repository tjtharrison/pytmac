from setuptools import setup

from _version import __version__

with open("README.md", encoding="UTF-8") as readme_file:
    readme_contents = readme_file.read()

with open("requirements.txt", encoding="UTF-8") as requirements_file:
    required = requirements_file.read().splitlines()

# Duplicate gpush.py to gpush
with open("tmac.py", "r", encoding="UTF-8") as tmac_file:
    tmac_contents = tmac_file.read()

with open("tmac", "w", encoding="UTF-8") as tmac_raw_file:
    tmac_raw_file.write(tmac_contents)

setup(
    name="tmac",
    version=__version__,
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    install_requires=required,
    scripts=[
        "tmac",
        "_version.py"
        ],
    packages=[
        "bin"
    ],
    package_data={
        "docs": ["*"]
    }
)
