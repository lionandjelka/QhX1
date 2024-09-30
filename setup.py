from setuptools import setup, find_packages

setup(
    name='QhX',  # Replace with our package's name
    version='0.1.1',  # Replace with our package's version
    author='Andjelka Kovacevic',  #  name
    author_email='andjelka.kovacevic@matf.bg.ac.rs',  # email
    description='A short description of our package',  # Provide a short description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LSST-SER-SAG-S1/QhX1',  # Replace with the URL of our package
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        'scikit-optimize',
        'libwwz',
        'colorednoise', 
        'tqdm',
        'panel',
        'hvplot',
        ' bokeh',
        'datashader',
        'pyarrow',
        'dask[dataframe]',
        'traitlets'
        
        # Add other dependencies required by our package
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Change as appropriate
        'Intended Audience :: Science/Research',  # Change as appropriate
        'License :: OSI Approved :: MIT License',  # Change as appropriate
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',  # Specify the minimum Python version required
    # Additional keywords about your package
    keywords='astronomy, data analysis, light curves',
    # Consider adding more configurations 
    project_urls={
        'Documentation': 'https://lionandjelka.github.io/QhX1/introduction.html',  # Add documentation URL here
    },
    
)
