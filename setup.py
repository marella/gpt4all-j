from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

name = 'gpt4all-j'

setup(
    name=name,
    version='0.2.5',
    description='Python bindings for the C++ port of GPT4All-J model.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ravindra Marella',
    author_email='mv.ravindra007@gmail.com',
    url='https://github.com/marella/{}'.format(name),
    license='MIT',
    packages=['gpt4allj'],
    package_data={'gpt4allj': ['lib/*/*.so', 'lib/*/*.dll', 'lib/*/*.dylib']},
    install_requires=[],
    extras_require={
        'tests': [
            'pytest',
        ],
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='{} gpt4all gpt-j ai llm cpp'.format(name),
)
