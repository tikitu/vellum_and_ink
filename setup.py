from setuptools import setup, find_packages
import os

version = '0.1.dev.0'

setup(
    name='vellum',
    version=version,
    description="Messing around with Hal Duncan's /Vellum/ and /Ink/",
    long_description='',
    classifiers=[],
    keywords='',
    author='Tikitu de Jager',
    author_email='tikitu+vellum@logophile.org',
    license='BSD',
    include_package_data=True,
    package_data={'vellum': ['clipped.html']},
    packages=['vellum'],
    zip_safe=False,
    install_requires=[
        'beautifulsoup4',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'vellum = vellum.tools:expand_vellum',
        ],
    },
)
