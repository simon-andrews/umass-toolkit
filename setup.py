import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="UMass Toolkit",
    version="0.0.1",
    author="Simon Andrews",
    author_email="sbandrews@umass.edu",
    description="Unofficial tools for interacting with various UMass APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simon-andrews/umass-toolkit",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'beautifulsoup4', 'pint'],
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    )
)
