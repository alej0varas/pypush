from setuptools import setup
import os


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(
    name="pypn",
    version="0.9",
    author="Alexandre Varas",
    author_email="alej0varas@gmail.com",
    py_modules=['pypn', ],
    include_package_data=True,
    license='GNU Library or Lesser General Public License (LGPL)',
    description="Abstraction library to send push notifications through APNs, GCM and OneSignal",
    long_description=README,
    url='https://github.com/alej0varas/pypn',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    keywords='push notification notifications apns gcm onesignal google apple',
)
