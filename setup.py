from setuptools import find_packages, setup

with open("README.md", 'r') as file:
    long_description = file.read()

setup(
    name="grouped_stratified_split",
    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/guides/single-sourcing-package-version/
    version="0.0.1",
    description="Grouped Stratified Split",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpmedras/grouped_stratified_split",
    author="Felipe Ferreira Marra and João Pedro Medrado Sena",
    author_email="felipeferreiramarra@gmail.com",
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Dataset Split Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
    ],
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a list of additional keywords, separated
    # by commas, to be used to assist searching for the distribution in a
    # larger catalog.
    keywords="dataset, split, stratified, grouped",  # Optional
    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    package_dir={"": "src"},
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(where="src"),  # Required
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.7, <4",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/discussions/install-requires-vs-requirements/
    install_requires=["pandas>=2.2.2","openpyxl>=3.1.4"],  # Optional
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional
    #    "dev": ["check-manifest"],
        "test": ["pytest>=8.2.2"],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #package_data={  # Optional
    #    "sample": ["package_data.dat"],
    #},
    # Entry points. The following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    #entry_points={  # Optional
    #    "console_scripts": [
    #        "sample=sample:main",
    #    ],
    #},
    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        "Bug Reports": "https://github.com/jpmedras/priority_group_stratified_split/issues",
    #    "Funding": "https://donate.pypi.org",
    #    "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/jpmedras/priority_group_stratified_split",
    },
)