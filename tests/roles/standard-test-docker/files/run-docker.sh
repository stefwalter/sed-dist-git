#!/bin/sh

ARTIFACTS_DIR=
DOCKER_IMAGE=
DOCKER_LOG=
PLAYBOOK=

usage() {
    if [ $# -ne 0 ]
    then
        echo "Error: $*" 1>&2
    fi
    echo "Usage: $(basename $0) -i image-name -a artifacts-dir -l docker-log -p playbook" 1>&2
    exit 2
}

while getopts a:hi:l:p: name
do
    case $name in
    a)   ARTIFACTS_DIR="$OPTARG" ;;
    i)   DOCKER_IMAGE="$OPTARG" ;;
    l)   DOCKER_LOG="$OPTARG" ;;
    p)   PLAYBOOK="$OPTARG" ;;
    h|*) usage ;;
    esac
done

shift $(($OPTIND - 1))

[ $# -eq 0 ] || usage "extraneous arguments found"

if [ -z "$DOCKER_IMAGE" -o -z "$ARTIFACTS_DIR" -o -z "$DOCKER_LOG" -o -z "$PLAYBOOK" ]
then
    usage "image-name, artifacts-dir, docker-log, and playbook must be provided"
fi

if [ ! -d "$ARTIFACTS_DIR" ]
then
    usage "artifacts-dir $ARTIFACTS_DIR must exist"
fi

if [ ! -f "$PLAYBOOK" ]
then
    usage "playbook $PLAYBOOK must exist"
fi

PLAYBOOK_BASE=$(basename "$PLAYBOOK")
PLAYBOOK_DIR=$(dirname "$PLAYBOOK")
PLAYBOOK_DIR=$(cd "$PLAYBOOK_DIR" ; pwd)

# set bind-mounts to playbook and artifact directories
DOCKER_MOUNTS=""
DOCKER_MOUNTS="$DOCKER_MOUNTS -v $PLAYBOOK_DIR:/playbooks:z,ro"
DOCKER_MOUNTS="$DOCKER_MOUNTS -v $ARTIFACTS_DIR:/artifacts:z,rw"

docker run -i --rm=true $DOCKER_MOUNTS "$DOCKER_IMAGE" /bin/sh -ex >>$DOCKER_LOG 2>&1 <<EOF

dnf install -y ansible python2-dnf libselinux-python

export ANSIBLE_CONFIG=/tmp/.ansible.cfg
echo '[defaults]' > \$ANSIBLE_CONFIG
echo 'retry_files_enabled = False' >> \$ANSIBLE_CONFIG

export DOCKER=1
ansible-playbook "/playbooks/$PLAYBOOK_BASE" -i localhost, -c local -e "artifacts=/artifacts"

EOF
