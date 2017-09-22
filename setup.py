from distutils.core import setup

setup(
      name='instantnews',
      version='1.0.7',
      description='Get live news instantaneously',
      author='shivam singh',
      author_email='shivam043@gmail.com',
      url='https://github.com/shivam043/instantnews',
      license='MIT',
      py_modules=['instantnews'],
      install_requires=[
      'requests','colored'
      ],
      entry_points='''
      [console_scripts]
      instantnews=instantnews:parser
      ''',
      
)
      
