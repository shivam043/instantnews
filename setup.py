from distutils.core import setup


with open('requirements.txt') as fobj:
    install_requires = [line.strip() for line in fobj]


setup(
      name='instantnews',
      version='1.2.4',
      description='Get live news instantaneously',
      author='shivam singh',
      author_email='shivam043@gmail.com',
      url='https://github.com/shivam043/instantnews',
      license='MIT',
      py_modules=['instantnews'],
      install_requires=install_requires,
      entry_points='''
      [console_scripts]
      instantnews=instantnews:parser
      ''',
)
