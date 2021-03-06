from distutils.core import setup

setup(
    name='ars',
    packages=["ars", "ars.behavior", "ars.core", "ars.db", "ars.utils"],
    version='0.2',
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
        'pyyaml',
        'scipy',
        'sqlalchemy',
        'psycopg2-binary'
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
