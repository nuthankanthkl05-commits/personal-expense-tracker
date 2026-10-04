from setuptools import setup, find_packages

setup(
    name="personal-expense-tracker",
    version="1.0.0",
    author="Vinay",
    description="A command-line based Personal Expense Tracker with analytics and visualization",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/personal-expense-tracker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "matplotlib>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "expense-tracker=main:main",
        ],
    },
)
