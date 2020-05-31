from Cython.Build import cythonize
from setuptools import setup, Extension
import Cython.Compiler.Options
Cython.Compiler.Options.annotate=True
import numpy, os, sys, os.path, tempfile, subprocess, shutil


def checkOpenmpSupport():
    """ Adapted from https://stackoverflow.com/questions/16549893/programatically-testing-for-openmp-support-from-a-python-setup-script
    """ 
    ompTest = \
    r"""
    #include <omp.h>
    #include <stdio.h>
    int main() {
    #pragma omp parallel
    printf("Thread %d, Total number of threads %d\n", omp_get_thread_num(), omp_get_num_threads());
    }
    """
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    filename = r'test.c'
    with open(filename, 'w') as file:
        file.write(ompTest)
    with open(os.devnull, 'w') as fnull:
        result = subprocess.call(['cc', '-fopenmp', filename],
                                 stdout=fnull, stderr=fnull)

    os.chdir(curdir)
    shutil.rmtree(tmpdir) 
    if result == 0:
        return True
    else:
        return False

if checkOpenmpSupport() == True:
    ompArgs = ['-fopenmp']
else:
    ompArgs = None 




#installation of PyStokes
setup(
    name='pystokes',
    version='1.0.1',
    url='https://github.com/rajeshrinet/pystokes',
    author = 'The PyStokes team',
    author_email = 'PyStokes@googlegroups.com',
    license='MIT',
    description='python library for computing Stokes flows',
    long_description='pystokes is a library for computing Stokes flows in various geometries',
    platforms='tested on LINUX',
    ext_modules=cythonize([ Extension("pystokes/*", ["pystokes/*.pyx"],
        include_dirs=[numpy.get_include()],
        extra_compile_args=ompArgs,
        extra_link_args=ompArgs,
        )],
        compiler_directives={"language_level": sys.version_info[0]},
        ),
    libraries=[],
    zip_safe = True,
    packages=['pystokes'],
    package_data={'pystokes': ['*.pxd']}
)

