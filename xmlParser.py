import os, sys
import re

from xml.etree import ElementTree

try:
	configRootDir = os.environ['configRootDir']
except:
	configRootDir = os.path.abspath(sys.argv[1])

XMLFILE = os.path.join(configRootDir, 'config.xml')

tree = ElementTree.parse(XMLFILE)

def get_sub_items(subTree, tag):
    srcPath=tree.findall(subTree)
    for i in srcPath:
        for t in list(i):
            if tag==t.tag:
                return t.text
	print "No tag %s available under %s, please check the configuration file %s" %(tag, subTree, XMLFILE)
    exit(1)

def getBspElement(bspName, kernelVer):
	bsp=tree.findall('bspName[@name="%s"][@kernelVer="%s"]' % (bspName, kernelVer))
	if len(bsp)==0:
		print "No bsp %s (%s) available, please check the configuration file %s" %(bspName, kernelVer, XMLFILE)
		exit(1)
	if len(bsp)>1:
		print "duplicated bsp %s (%s), please check the configure file %s" % (bspName, kernelVer, XMLFILE)
		exit(1)
	return bsp[0]

def getBspValueByTag(bspName, kernelVer, tag):
	bsp=getBspElement(bspName, kernelVer)
	for t in list(bsp):
		for i in t.items():
			if i[0]==tag:
				return i[1]
	print "No tag %s available for bsp %s (%s), please check the configuration file %s" %(tag, bspName, kernelVer, XMLFILE)
	exit(1)

def getUserToolchainByBsp(bspName, kernelVer):
	l=[]
	l.append(getBspValueByTag(bspName, kernelVer, 'busyboxToolchain'))
	l.append(getBspValueByTag(bspName, kernelVer, 'kernelToolchain'))
	return l

def listAllBsps():
	bsp=tree.findall('bspName')
	l={}
	for i in bsp:
		s=i.attrib['name'] + ' (' + i.attrib['kernelVer'] + ')'
		if l.has_key(s):
			print "duplicated bsp %s for kernel version %s, please check the configure file %s" % (i.attrib['name'], i.attrib['kernelVer'], XMLFILE)
			exit(1)
		l.update({s:1})
	return l

def get_all_user_toolchains():
	tc=tree.findall('bspName/toolchain')
	l={}
	for i in tc:
		if not l.has_key(i.attrib['busyboxToolchain']):
			l.update({i.attrib['busyboxToolchain']:1})
	return l

def get_all_kernel_toolchains():
	tc=tree.findall('bspName/toolchain')
	l={}
	for i in tc:
		if not l.has_key(i.attrib['kernelToolchain']):
			l.update({i.attrib['kernelToolchain']:1})
	return l

def get_all_toolchains():
	tc=tree.findall('bspName/toolchain')
	l={}
	for i in tc:
		if not l.has_key(i.attrib['kernelToolchain']):
			l.update({i.attrib['kernelToolchain']:1})
		if not l.has_key(i.attrib['busyboxToolchain']):
			l.update({i.attrib['busyboxToolchain']:1})
	return l

def get_kernel_versions():
	bsp=tree.findall('bspName')
	l={}
	for i in bsp:
		if not l.has_key(i.attrib['kernelVer']):
			l.update({i.attrib['kernelVer']:1})
	return l

def getBspInfo(bspName, kernelVer, ip=None):
	bsp=getBspElement(bspName, kernelVer)
	l=[]
	l.append('bspName=%s' % bspName)
	l.append('kernelVer=%s' % kernelVer)
	for t in list(bsp):
		for i in t.items():
			if ip and i[0]=="ipAddr":
				if not ip in i[1].split(','):
					print "The IP:%s does not belong to bsp:%s (%s)" % (ip, bspName, kernelVer)
					exit(1)
				s=i[0] + '=' + ip
			else:
				s=i[0] + '=' + i[1]
			l.append(s)
	return l

def getArchByToolchain(toolchain):
	bsp=tree.findall('bspName')
	for i in bsp:
		k=i.findall('kernel')
		t=i.findall('toolchain')
		if toolchain==t[0].attrib['kernelToolchain']:
			return k[0].attrib['arch']
	exit(1)

def getIpBspExtfsPairs():
	bsp=tree.findall('bspName')
	l=[]
	for i in bsp:
		for ip in i.findall('target')[0].attrib['ipAddr'].split(','):
			s=ip + '+' + i.attrib['name'] + '+'
			if i.findall('part'):
				s+=i.findall('part')[0].attrib['extStorage']
			l.append(s)
	return l

def getBspByIpExtfs(ip, extfs):
	bsp=tree.findall('bspName')
	for i in bsp:
		if ip in i.findall('target')[0].attrib['ipAddr'].split(','):
			if extfs in re.split('[,;:]', i.findall('part')[0].attrib['extStorage']):
				return i.attrib['name']
