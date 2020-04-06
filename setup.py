from distutils.core import setup

setup(
    name = 'biggu-container',
    packages = ['biggu-container'],
    version = '0.0.1',
    package_dir={'':'src'},
    exclude=["test"],
    description = 'IoC for python projects',
    author = 'Eduardo Salazar',
    author_email = 'eduardosalazar89@hotmail.es',
    url = 'https://github.com/esalazarv/biggu-container.git',
    download_url = 'https://github.com/esalazarv/biggu-container/archive/0.0.1.zip',
    keywords = ['container', 'IoC', 'dependencies', 'injection', 'resolution'],
    license="MIT",
    classifiers = [
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    install_requires=[],
)