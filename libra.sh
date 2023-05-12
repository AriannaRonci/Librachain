#!/bin/bash

echo ""
echo "==============================================="
echo '
    ___ __                    __          _     
   / (_) /_  _________ ______/ /_  ____ _(_)___ 
  / / / __ \/ ___/ __ `/ ___/ __ \/ __ `/ / __ \
 / / / /_/ / /  / /_/ / /__/ / / / /_/ / / / / /
/_/_/_.___/_/   \__,_/\___/_/ /_/\__,_/_/_/ /_/

    You are running librachain setup script!
'
echo "==============================================="
echo ""

read -p "Do you want to install librachain (y/n)?" select

if [ $select == "y" ];
then

	echo ""
	echo "==============================================="
	echo "           Checking python version 	     "
	echo "==============================================="
	echo ""

	if command -v python3 &> /dev/null
	then
		echo "python3 is installed"
	else
		echo "python3 not found, let's try python"
		if command -v python &> /dev/null
		then
			echo "python found, let's check version"
			if [ "$(python --version)" > "Python 3" ];
			then
				echo "Python version ok!"
			else
				echo "Python version not compatible, please install python3"
			fi
		fi
	fi

	echo ""
	echo "==============================================="
	echo "          Checking python requirements 	     "
	echo "==============================================="
	echo ""

	pip3 install -r Librachain/requrements.txt

	echo ""
	echo "==============================================="
	echo "          Setting up docker environment 	     "
	echo "==============================================="
	echo ""
	echo ""
	echo "==============================================="
	echo "          Setting up containers 	     	     "
	echo "==============================================="
	echo ""
fi

echo "Goodbye!"

