from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="exam-analyzer",
    version="1.0.0",
    description="Analyze previous year exam papers, predict high-probability topics, and generate practice questions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Exam Analyzer Team",
    python_requires=">=3.11",
    packages=find_packages(),
    package_data={
        "data": ["taxonomies/*.json"],
    },
    install_requires=[
        "streamlit>=1.30.0",
        "pdfplumber>=0.10.0",
        "PyMuPDF>=1.23.0",
        "pandas>=2.1.0",
        "numpy>=1.25.0",
        "plotly>=5.18.0",
        "openpyxl>=3.1.0",
        "reportlab>=4.0.0",
        "openai>=1.10.0",
        "google-generativeai>=0.3.0",
        "requests>=2.31.0",
        "pytesseract>=0.3.10",
        "pdf2image>=1.16.0",
        "Pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "exam-analyzer=app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Education",
    ],
)
