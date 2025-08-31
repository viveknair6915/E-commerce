from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy as np

# Define the extension with numpy include directories
extensions = [
    Extension(
        "core.recommendations.similarity",
        ["core/recommendations/similarity.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"],  # Optimize for speed
        language="c++",
    )
]

setup(
    name="recommendations",
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
    zip_safe=False,
)
