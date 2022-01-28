from distutils.core import setup
setup(
    name='AgentRoutingSimulator',         
    packages=['agentrouting'],
    version='0.1',                
    license='GLP3',
    description='TYPE YOUR DESCRIPTION HERE',
    author='Melvyn Linke',
    author_email='Melvyn.linke@web.de',   
    url='https://github.com/user/reponame',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['Multi Agent Systems', 'Networking', 'Simulation'],
    install_requires=[     
        'networkx',
        'pytest',
        'numpy'
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
