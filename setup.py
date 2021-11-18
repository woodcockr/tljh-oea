from setuptools import setup

setup(
    name="tljh-oea",
    author="woodcockr",
    version="0.0",
    license="APACHEv2",
    url='https://github.com/woodcockr/tljh-oea',
    entry_points={"tljh": ["oea = tljh_oea"]},
    py_modules=["tljh_oea"],
)