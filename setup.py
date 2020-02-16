from setuptools import setup

install_requires = []
with open('requirements.txt', 'r') as requirements:
  install_requires = requirements.read().splitlines()

with open('README.md', 'r') as readme:
    long_description = readme.read()

with open('LICENSE', 'r') as license_text:
    license = license_text.read()

setup(name='gsb',
      author='Elijah Woodward',
      url='https://github.com/ElbowBaggins/gpm-spoofy-bot',
      version='0.0.1',
      license=license,
      description='A Discord bot for converting Google Play Music links to Spoofy links, in Python. For some reason.',
      long_description=long_description,
      long_description_content_type='text/x-markdown',
      install_requires=install_requires,
      python_requires='>=3.8.1'
)
