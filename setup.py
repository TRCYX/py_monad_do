import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='monad_do',
    version='0.1.1',
    author='TRCYX',
    license='MIT',
    description='Do notation in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TRCYX/py_monad_do',
    packages=['monad_do'],
    install_requires=['fastcache'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries',
        # 'Typing :: TypedTyping :: Typed'
    ],
    keywords='monad'
)
