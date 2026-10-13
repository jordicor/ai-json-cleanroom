"""Setup configuration for ai-json-cleanroom."""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-json-cleanroom",
    version="1.2.0",
    author="AI JSON Cleanroom Contributors",
    description="Robust post-processing layer for AI-generated JSON outputs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jordicor/ai-json-cleanroom",
    py_modules=["ai_json_cleanroom"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    extras_require={
        "fast": ["orjson>=3.0.0"],
    },
    keywords=[
        "llm",
        "json",
        "validation",
        "ai",
        "openai",
        "anthropic",
        "claude",
        "gpt",
        "parsing",
        "repair",
        "post-processing",
        "structured-output",
    ],
    project_urls={
        "Bug Reports": "https://github.com/jordicor/ai-json-cleanroom/issues",
        "Source": "https://github.com/jordicor/ai-json-cleanroom",
    },
)
