#     Copyright 2015 Netflix, Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
from setuptools import setup

setup(
    name='sleepypuppy',
    version='0.2',
    long_description=__doc__,
    packages=['sleepypuppy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.10.1',
        'WTForms==2.0.2',
        'Flask-Admin==1.2.0',
        'Flask-Bcrypt==0.6.2',
        'Flask-Login==0.2.11',
        'Flask-Mail==0.9.1',
        'Flask-RESTful==0.3.4',
        'Flask-SQLAlchemy==2.0',
        'Flask-Script==2.0.5',
        'Flask-WTF==0.11',
        'Pillow==2.8.2',
        'SQLAlchemy==1.0.5',
        'bcrypt==2.0.0',
        'gunicorn==19.3.0',
        'psycopg2==2.6.1',
        'boto==2.38.0',
        'BeautifulSoup',
        'flask-migrate'
    ]
)
