"""Setup manifest."""
from setuptools import setup, find_packages

setup(
    name="MKVTag",
    version="0.1",
    description="Frontend wrapper script for setting MKV title meta " +
                "property using mkvpropedit (part of the mkvtoolnix suite).",
    keywords="mkv filename title mkvpropedit mkvtoolnix wrapper",
    url="https://github.com/ylabonte/mkvtag",
    author="Yannic Labonte",
    author_email="yannic.labonte@gmail.com",
    packages=find_packages(),
    scripts=['bin/mkvtag'],
)
