from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

name = 'gpt4all-j'

setup(
    name=name,
    version='0.1.1',
    description='Python bindings for the C++ port of GPT4All-J model.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    package_data={'gpt4allj': ['**/*.so', '**/*.dll', '**/*.dylib']},
    install_requires=[],
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='{}'.format(name),
)
