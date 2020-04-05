docker network create wackywangonet

docker build -f docker/Dockerfile . -t wackywangoimage

docker run --network=wackywangonet --name postgres-server -d -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password postgres
docker run --network=wackywangonet --name rabbitmq-server -d -p 5672:5672 rabbitmq

mkdir data
mkdir data/raw_data
mkdir data/pics
mkdir data/pics/color_image
mkdir data/pics/depth_image

#This is used to serve the images by the GUI server
ls -l pics/color_image/

docker run --rm --detach --network=wackywangonet -p 8000:8000 -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.server run-server -h '0.0.0.0' -p 8000 'rabbitmq://rabbitmq-server:5672/'"
docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.parsers run-parser 'color_image' 'rabbitmq://rabbitmq-server:5672/'"
docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.parsers run-parser 'depth_image' 'rabbitmq://rabbitmq-server:5672/'"
docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.parsers run-parser 'pose' 'rabbitmq://rabbitmq-server:5672/'"
docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.parsers run-parser 'feelings' 'rabbitmq://rabbitmq-server:5672/'"
docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.saver run-saver  'postgresql://postgres-server:5432' 'rabbitmq://rabbitmq-server:5672/'"
docker run --rm --detach --network=wackywangonet -p 5000:5000 -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.api run-server -h '0.0.0.0' -p 5000 -d 'postgresql://postgres-server:5432'"


#
#sudo docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.parsers run-parser 'color_image' 'rabbitmq://rabbitmq-server:5672/'"
#sudo docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.parsers run-parser 'depth_image' 'rabbitmq://rabbitmq-server:5672/'"
#sudo docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.parsers run-parser 'pose' 'rabbitmq://rabbitmq-server:5672/'"
#sudo docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.parsers run-parser 'feelings' 'rabbitmq://rabbitmq-server:5672/'"
#sudo docker run --rm --detach --network=wackywangonet -v $PWD/data/:/tmp/wackywangodata wackywangoimage  /bin/bash -c "python -m wackywango.saver run-saver  'postgresql://postgres-server:5432' 'rabbitmq://rabbitmq-server:5672/'"
