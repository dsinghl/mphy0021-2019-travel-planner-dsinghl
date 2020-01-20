from distutils.core import setup

setup(
    name="travelplanner",
    description="A travelplanner package to calulate bus journeys",
    version="0.1.0",
    install_requires=["matplotlib", "numpy"],
    packages=["travelplanner"],
    license="OSI Approved :: MIT License",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Deep Singh Lall",
    author_email="deep.lall.19@ucl.ac.uk",
    entry_points={"console_scripts": ["bussimula=travelplanner.command:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Journey planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3",
)
