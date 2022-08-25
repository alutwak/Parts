from setuptools import setup, find_packages

requirements = ["digikey-api", "openpyxl", "PyYaml"]

setup(name="Parts",
      description="A library for managing electronic parts",
      author="Ayal Lutwak",
      author_email="ayal@audio-electric.com",
      platforms=["linux", "mac", "windows"],
      install_requires=requirements,
      packages=find_packages(exclude=["__main__"]),
      entry_points="""
      [console_scripts]
      addparts=addparts:main
      printpart=printpart:main
      resheetparts=resheetparts:main
      """)
