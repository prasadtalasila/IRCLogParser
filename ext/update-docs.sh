echo "\nBuild Complete"
echo "\n================Updating gh-pages================ \n"
while true; do
    read -p "Do you wish to update gh-pages (yes/no)? " yn
    case $yn in
        [Yy]* ) 
		cd ..
		echo "================ Adding relevent files ================s"
		touch docs/build/html/.nojekyll
		git add docs/build/html/
		git add -f docs/build/html/.nojekyll
		echo "================ Commiting the changes ================"
		git commit -m "[Automatic] Update Documentation"
		echo "================ Pushing the commit to gh-pages ================"
		git subtree push --prefix docs/build/html origin gh-pages
		echo "================ Push Complete | Documentation Updated at gh-pages ================"
		break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done


