DL_ENV=${1:-"keras"}
NOTEBOOK_PORT=${2:-8888}
VISDOM_PORT=${3:-8097}
PYTORCH_IMAGE=pytorch:0.4.1-py3-gpu
KERAS_IMAGE=keras_latest

if [ "$DL_ENV" = "pytorch" ]; then
    echo 'using pytorch'
    if [ ! $(docker images -q ${PYTORCH_IMAGE}) ]; then
        echo 'in if'
        docker build . -t ${PYTORCH_IMAGE} -f ./docker/Dockerfile.pytorch
    fi
    # this should run a pytorch notebook container
    echo 'post if'
    docker run --runtime=nvidia --shm-size 8G -v `pwd`:/workspace -p ${NOTEBOOK_PORT}:8888 -p ${VISDOM_PORT}:8097 --name pytorch_notebook ${PYTORCH_IMAGE}
    docker exec pytorch_notebook jupyter notebook list
elif [ "$DL_ENV" = "keras" ]; then
    echo 'using keras'
    if [ ! $(docker images -q ${KERAS_IMAGE}) ]; then
        echo 'in if'
        docker build . -t ${KERAS_IMAGE} -f ./docker/Dockerfile.keras
    fi
    # this should run a keras notebook container
    echo 'post if'
    docker run --runtime=nvidia --shm-size 8G -v `pwd`:/workspace -p ${NOTEBOOK_PORT}:8888 -p ${VISDOM_PORT}:8097 --name keras_notebook ${KERAS_IMAGE}
    docker exec keras_notebook jupyter notebook list
else
    echo 'no valid DL_ENV provided'
    exit 1
fi
