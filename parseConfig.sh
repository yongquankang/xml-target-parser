#!/bin/sh

# 10209416 10/02/2017 initial version, provide APIs for parsing xml configurations
# 10209416 15/03/2017 implement xml parser in python
export PYTHONPATH=$configRootDir

getLinkValueByTag()
{ # $1 tag
	python -c "import xmlParser as xmlParser;print xmlParser.get_sub_items(\"srcPath\", \"$1\")"
}

getServerConfByTag()
{ # $1 tag
	python -c "import xmlParser as xmlParser;print xmlParser.get_sub_items(\"serverConf\", \"$1\")"
}

getBspValueByTag()
{ # $1=bspName, $2=kernelVer, $3=tag
	python -c "import xmlParser as xmlParser;print xmlParser.getBspValueByTag(\"$1\", \"$2\", \"$3\")"
}

getConfigsByBspIp()
{ # $1=bspName, $2=kernelVer, $3 ip address
python -c "import xmlParser as xmlParser
for i in xmlParser.getBspInfo(\"$1\", \"$2\", \"$3\"):
	print i
"
}

listAllBsps()
{
python -c "import xmlParser as xmlParser
for i in xmlParser.listAllBsps():
	print i
"
}

getArchByToolchain()
{
	python -c "import xmlParser as xmlParser;print xmlParser.getArchByToolchain(\"$1\")"
}

getAllUsrToolchainPairs()
{ # kernel toolchains are included
python -c "import xmlParser as xmlParser
for i in xmlParser.get_all_toolchains():
	print i
"
}

getAllKernelToolchainPairs()
{
python -c "import xmlParser as xmlParser
for i in xmlParser.get_all_kernel_toolchains():
	print i
"
}
getSupportedKernel()
{
python -c "import xmlParser as xmlParser
for i in xmlParser.get_kernel_versions():
	print i
"
}

getIpBspExtfsPairs()
{
python -c "import xmlParser as xmlParser
for i in xmlParser.getIpBspExtfsPairs():
	print i
"
}

getLinuxBaselineByBsp()
{
	python -c "import xmlParser as xmlParser;print xmlParser.getBspValueByTag(\"$1\", \"$2\", \"baseline\")"
}

getBspByIpExtfs()
{ #ip=$1, $extfs=$2
	python -c "import xmlParser as xmlParser;xmlParser.getBspByIpExtfs(\"$1\", \"$2\")"
}
