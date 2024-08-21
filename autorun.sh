image_name=oschan77/lscm_unimap_pgm2pbstream:latest
instance_name=pgm2pbstream

check_docker_instance_already_running() {
    if  [ ! "$(docker ps -a | grep $instance_name)" ]; then
        return 0
    fi
    return 1
}

delete_running_docker_instance() {
    if ! docker container rm --force "${instance_name}"; then
        return 1
    fi
    return 0
}


simulation_main() {
    xhost +local:docker               # allow window
    if ! check_docker_instance_already_running; then
        if ! delete_running_docker_instance; then
            return 1
        fi
    fi
    # docker build -t $image_name . 
    
    docker run -itd \
        --name $instance_name \
        --gpus all \
        --env NVIDIA_DRIVER_CAPABILITIES=all \
        --env DISPLAY=${DISPLAY} \
        --env QT_X11_NO_MITSHM=1 \
        --device=/dev/dri \
        --group-add video \
        --device=/dev/snd:/dev/snd \
        --group-add audio \
        --net=host \
        --privileged \
        --volume /tmp/.X11-unix:/tmp/.X11-unix \
        --volume="$HOME/.Xauthority:/root/.Xauthority" \
        --volume="$(pwd)/workspace:/root/workspace" \
        $image_name /bin/zsh    
}

simulation_main