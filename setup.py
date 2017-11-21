from distutils.core import setup

setup(
    name='scratch_minetest_turle',
    version='0.1.0',
    author='Albert Caramia',
    author_email='@github',
    packages=['scratch_minetest_turle'],
    scripts=[],
    url='https://github.com/acaramia/scratch_minetest_turtle',
    license='LICENSE.txt',
    description='Scracth extension for a simple turtle in Minetest',
    long_description=open('README.txt').read(),
    install_requires=[
        "Flask",
        "pycraft-minetest",
    ],
)
