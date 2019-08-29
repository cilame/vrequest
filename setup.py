from setuptools import setup
import vrequest
 
setup(
    name = "vrequest",
    version = vrequest.__version__,
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

    packages = [
        "vrequest",
    ],
    package_data ={
        "vrequest":[
            'template/*',
            'template/v/*',
            'template/v/spiders/*',
            'ico.ico'
        ]
    },
    python_requires=">=3.6",
    install_requires=[
       'requests',
       'lxml',
    ],
    entry_points={
        'gui_scripts': [
            'vv = vrequest.main:execute',
            'vrequest = vrequest.main:execute',
            'ee = vrequest.main:algo',
        ]
    },
)