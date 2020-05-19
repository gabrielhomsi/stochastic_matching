from setuptools import setup, find_packages

setup(
    name="stochastic_matching",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Gabriel Homsi",
    install_requires=["numpy", "icecream", "click", "gurobipy", "matplotlib", "seaborn"]
)
