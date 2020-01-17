# author        :   ignorantshr
# create_date   :   2020/01/17 11:22 AM
# description   :   

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),   # find python package automatically
    include_package_data=True,  # include data file, such as static and
                                # templates. according to MANIFEST.in
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
