from setuptools import setup

# Setup for the 'salah_rent' app
setup (
	name 					= 'salah_rent'
	, packages 				= ['salah_rent']
	, include_package_data 	= True
	, install_requires 		= ['flask']
)