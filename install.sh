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
		python_command=python3
		echo "python3 is installed"
	else
		echo "python3 not found, let's try python"
		if command -v python &> /dev/null
		then
			echo "python found, let's check version"
			if [ "$(python --version)" > "Python 3" ];
			then
				python_command=python
				echo "Python version ok!"
			else
				echo "Python version not compatible, please install python3"
				exit
			fi
		fi
	fi

	echo ""
	echo "==============================================="
	echo "          Checking python requirements 	     "
	echo "==============================================="
	echo ""

	! $python_command -m pip install -r requirements.txt && exit

	echo ""
	echo "==============================================="
	echo "          Setting up docker environment 	     "
	echo "==============================================="
	 
	shards_numbers=$(grep "shards_number" config/configuration.yml | grep -o "[0-9]")
	regex="shard[1-$shards_numbers]+"
	services=$(grep -oE "$regex" docker-compose.yml | uniq | tr '\n' ' ')
	! docker-compose up -d $services &&  exit
	
	echo "" 
	echo ""
	echo "==============================================="
	echo "          Setting up containers 	     	     "
	echo "==============================================="
	echo ""

	$python_command deploy_on_chain.py
	$python_command set_up.py
	$python_command main.py
		
fi

echo "Goodbye!"
