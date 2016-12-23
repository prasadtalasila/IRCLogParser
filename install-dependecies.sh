echo "Updating Package list to install latest dependencies"
#Update package lists to retrieve latest version of packages
sudo apt-get update

echo "Installing Python Index Package (pip)."
echo "We will require pip to install some of the dependencies"
#install Python Index Package
sudo apt-get install python-pip
sudo pip install --upgrade pip

echo "--------------------------------------------------------"
echo "### Installing package dependencies for IRC LogParser ###"
echo "--------------------------------------------------------"

echo "Installing networkx"
#Install newtworkx package
wget https://github.com/networkx/networkx/archive/networkx-1.8.1.tar.gz
tar -xvzf networkx-1.8.1.tar.gz
cd ./networkx-networkx-1.8.1
sudo python ./setup.py install
cd ..
sudo rm -rf ./networkx-1.8.1.tar.gz
sudo rm -rf ./networkx-networkx-1.8.1
echo "Finished installing networkx"

echo "--------------------------------------------------------"
echo "Installing numpy"
#Install numpy
sudo apt-get install python-numpy
echo "Finished installing numpy"

echo "--------------------------------------------------------"
echo "Installing Matplotlib"
#Install Matplotlib
sudo apt-get install python-matplotlib
echo "Finished installing Matplotlib"

echo "--------------------------------------------------------"
echo "Installing pygraphviz"
#Install pygraphviz
git clone https://github.com/pygraphviz/pygraphviz.git
cd pygraphviz
sudo python ./setup.py install
cd ..
sudo rm -rf pygraphviz
echo "Finished installing pygraphviz"

echo "--------------------------------------------------------"
echo "Installing scipy and scikit learn"
#Install scipy and sklearn
sudo apt-get install python-scipy
pip install -U scikit-learn
echo "Finished installing scipy and scikit learn"

echo "--------------------------------------------------------"
echo "Installing NLTK and NLTK-Data"
echo "Please Wait!!. This may take some time "

#Install Natural Language Toolkit
sudo pip install -U nltk
python -c "import nltk;nltk.download('wordnet');"
echo "Finished installing NLTK and NLTK-Data"

echo "--------------------------------------------------------"
echo "Installing Python Pandas"
#Install pandas
sudo apt-get install python-pandas
echo "Finished installing Python-Pandas"

echo "--------------------------------------------------------"
echo "### Finished Installing package dependencies for IRC LogParser ###"
echo "If you recieved Error message, try following the message to resolve the issue and the re-run this script"
echo "Or you can also try installing that library manually"
echo "--------------------------------------------------------"
