import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='PyHistopathology',  

     version='0.1',

     scripts=['WSI_Patch_Extraction.py'] ,

     author="Sai Chandra",

     author_email="deepak.kumar.iet@gmail.com",

     description="A WSI Image processing application",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/saichandra1/PyHistopathology",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",

         "Operating System :: OS Independent",

     ],

)
