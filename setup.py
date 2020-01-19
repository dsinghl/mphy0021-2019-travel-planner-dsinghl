from distutils.core import setup

setup(
    name='tplanner',
    description='A travelplanner package to calulate bus journeys',
    version='0.1',
    install_requires=['matplotlib','numpy',],
    packages=['travelplanner'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    entry_points={
        "console_scripts": [
            "bussimula=travelplanner.__main__:main",
        ]
    },
)
