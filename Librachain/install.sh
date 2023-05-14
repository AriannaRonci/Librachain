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
		$py = 0
		echo "python3 is installed"
	else
		echo "python3 not found, let's try python"
		if command -v python &> /dev/null
		then
			echo "python found, let's check version"
			if [ "$(python --version)" > "Python 3" ];
			then
				$py = 1
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

	pip install -r requirements.txt

	echo ""
	echo "==============================================="
	echo "          Setting up docker environment 	     "
	echo "==============================================="
	
	docker-compose up -d
	
	echo "" 
	echo ""
	echo "==============================================="
	echo "          Setting up containers 	     	     "
	echo "==============================================="
	echo ""

	if [ $py==0 ];
		then python3 deploy_on_chain.py
		     python3 set_up.py
		     python3 main.py
		
	fi
fi

echo "Goodbye!"
