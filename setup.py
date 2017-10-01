from setuptools import setup

setup(
      name='instantnews',
      version='1.2.0',
      description='Get live news instantaneously',
      author='shivam singh',
      author_email='shivam043@gmail.com',
      url='https://github.com/shivam043/instantnews',
      license='MIT',
      py_modules=['instantnews'],
      install_requires=[
      'requests'
      ],
      entry_points='''
      [console_scripts]
      instantnews=instantnews:parser
      ''',
      
)
      
