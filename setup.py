import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mechcalc",
    version="1.2",
    author="Chuck McKyes",
    author_email="cmckyes@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    # packages=setuptools.find_packages(),
    packages=['mechcalc'],
    install_requires=[
          'wheel',
          'wxPython==4.0.7.post2',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
