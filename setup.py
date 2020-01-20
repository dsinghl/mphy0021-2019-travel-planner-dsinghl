from distutils.core import setup

setup(
    name="travelplanner",
    description="A travelplanner package to calulate bus journeys",
    version="0.1",
    install_requires=["matplotlib", "numpy"],
    packages=["travelplanner"],
    license="OSI Approved :: MIT License",
    long_description=open("README.md").read(),
    entry_points={"console_scripts": ["bussimula=travelplanner.command:main"]},
)
