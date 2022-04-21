from setuptools import setup, find_packages
setup(
    name='AgentRoutingSimulator',
    packages=find_packages("AgentRoutingSimulator"),
    version='0.1',
    license='GLP3',
    description='TYPE YOUR DESCRIPTION HERE',
    author='Melvyn Linke',
    author_email='Melvyn.linke@web.de',
    url='https://github.com/MelVimL/AgentRoutingSimulator',
    download_url='https://github.com/MelVimL/AgentRoutingSimulator.git',
    keywords=['Multi Agent Systems', 'Networking', 'Simulation'],
    install_requires=[
        'networkx',
        'pytest',
        'numpy',
        'pyyaml'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers :: Students',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GLP3 License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
