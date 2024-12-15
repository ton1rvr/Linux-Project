docker build --build-arg APP_VERSION=$1 -t my_app .
docker run -d -p 5005:5005 my_app
echo click on this link !! http://23.100.8.30:5005
