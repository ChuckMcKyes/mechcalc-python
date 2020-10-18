import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mechcalc",
    version="1.2.2",
    author="Chuck McKyes",
    author_email="cemckyes@gmail.com",
    description="Mechanical Engineering Calculators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    # packages=setuptools.find_packages(),
    packages=['mechcalc'],
    # to include data files:
    package_dir={'mechcalc':'mechcalc'},
    package_data={
      'mechcalc': ['data/*.png'],
    },
    install_requires=[
          'wheel',
          'wxPython',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
