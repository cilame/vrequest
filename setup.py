from setuptools import setup
 
setup(
    name = "vrequest",
    version = "1.1.3",

    keywords = "vrequest",
    author = "cilame",
    author_email = "opaquism@hotmail.com",
    url="https://github.com/cilame/vrequest",
    license = "MIT",
    description = "",
    long_description = '',
    long_description_content_type="text/markdown",
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],

    packages = ["vrequest"],
    python_requires=">=3.6",
    install_requires=[
       'requests',
       'lxml',
    ],

    entry_points={
        'gui_scripts': [
            'vv = vrequest.main:execute',
            'vreqeust = vrequest.main:execute',
        ]
    },
)