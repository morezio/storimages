# build the image and remove the dangling previous to keep it clean at the terminal
docker build -t morezio/storimages:fe_dev -f frontend.dockerfile .
echo 'y' | docker image prune