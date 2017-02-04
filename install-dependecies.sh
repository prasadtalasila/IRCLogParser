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
sudo pip install networkx
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
sudo apt-get install graphviz libgraphviz-dev pkg-config
sudo apt-get install python-pip python-virtualenv
sudo pip install pygraphviz
echo "Finished installing pygraphviz"

echo "--------------------------------------------------------"
echo "Installing scipy and scikit learn"
#Install scipy and sklearn
sudo apt-get install python-scipy
sudo pip install -U scikit-learn
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
echo "Installing Sphinx documentation and it's dependencies"
#Install Sphinx
sudo pip install --upgrade pip
sudo pip install --upgrade sphinx
sudo pip install --upgrade pyyaml
sudo pip install --upgrade t3SphinxThemeRtd
sudo pip install --upgrade t3fieldlisttable
sudo pip install --upgrade t3tablerows
sudo pip install --upgrade t3targets
sudo pip install --upgrade sphinxcontrib-googlechart
sudo pip install --upgrade sphinxcontrib-googlemaps
sudo pip install --upgrade sphinxcontrib-httpdomain
sudo pip install --upgrade sphinxcontrib-slide
sudo pip install --upgrade sphinxcontrib.youtube
echo "Finished installing Sphinx"

echo "--------------------------------------------------------"
echo "### Finished Installing package dependencies for IRC LogParser ###"
echo "If you recieved Error message, try following the message to resolve the issue and the re-run this script"
echo "Or you can also try installing that library manually"
echo "--------------------------------------------------------"
