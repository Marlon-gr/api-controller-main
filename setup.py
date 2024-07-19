# -*- encoding: utf-8 -*-
# Source:
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import io
import re

from setuptools import find_packages, setup

dev_requirements = [
    'bandit',
    'flake8',
    'isort',
    'pytest'
]
unit_test_requirements = [
    'pytest',
]
integration_test_requirements = [
    'pytest',
]
run_requirements = [
    'flask==2.2.4', 'gunicorn==20.0.4', 'flask-swagger-ui==3.25.0',
    'pyyaml==5.3.1', 'prometheus_client==0.8.0', 'requests==2.24.0',
    'aiohttp==3.6.2', 'gevent==20.6.2', 'Flask-Opentracing', 'jaeger-client'
]

with io.open('api_controller/__init__.py', encoding='utf8') as version_f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with io.open('README.md', encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="api_controller",
    version=version,
    author="Marlon Gonzalez Ramirez",
    author_email="glezmarlon0@gmail.com",
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    url=""
        "api-controller",
    license="COPYRIGHT",
    description="",
    long_description=long_description,
    zip_safe=False,
    install_requires=run_requirements,
    extras_require={
         'dev': dev_requirements,
         'unit': unit_test_requirements,
         'integration': integration_test_requirements,
    },
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=(),
    entry_points={
        'console_scripts': [
            'api_controller = api_controller.main:app'
        ],
    },
)
