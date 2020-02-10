.. PyHistopathology documentation master file, created by
   sphinx-quickstart on Sun Feb  9 08:14:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyHistopathology
=================

PyHistopathology is a Python API for pre-processing Whole-Slide Images for use in a machine learning algorithm.

Features
=========

Reading Whole-Slide Images with WSI_Scanning.readWSI() 

* Input: WSI path or directory
* Output: Numpy array of WSI with data type int32

Denoising Whole-Slide Images with Denoising.denoising()

* Input: WSI Path or directory
* Output: Numpy array of WSI Image (After denoising) with dtype int32

Patch Extraction for Whole-Slide Images with Extractingpatches.extractingPatches()

* Input: WSI Path or directory
* Output: Fills up the outputpath with patches extracted from the WSI



Table of Contents
==================
.. toctree::
   :maxdepth: 2

   reading
   denoising
   extracting
