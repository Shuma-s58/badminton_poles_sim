from setuptools import setup
from glob import glob
package_name='badminton_poles_sim'
setup(name=package_name, version='0.1.1', packages=[package_name], data_files=[('share/ament_index/resource_index/packages',['resource/'+package_name]),('share/'+package_name,['package.xml']),('share/'+package_name+'/launch',glob('launch/*.py')),('share/'+package_name+'/rviz',glob('rviz/*.rviz'))], install_requires=['setuptools'], zip_safe=True, maintainer='maintainer', maintainer_email='maintainer@example.com', description='RViz badminton pole visualization', license='Apache-2.0', entry_points={'console_scripts':['sim = badminton_poles_sim.sim:main']})
