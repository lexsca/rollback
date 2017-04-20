from setuptools import setup

setup(
  name='rollback',
  version='1.0.5',
  description='Simple rollback mechanism',
  author='Lex Scarisbrick',
  author_email='lex@scarisbrick.org',
  license='MIT',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  url='https://github.com/lexsca/rollback',
  py_modules=['rollback'],
  tests_require=['mock', 'nose'],
  test_suite='nose.collector'
)
