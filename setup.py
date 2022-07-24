import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='dlin',
    url='https://github.com/elliottkobelansky/dlin',
    author='Elliott Kobelansky',
    packages=['dlin'],
    scripts=['dlin-trace'],
    version='0.1.0',
    license='MIT',
    description="Describe the cycles on a scrambled Rubik's Cube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ["numpy"],
)    
    
