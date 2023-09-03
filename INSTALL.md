# kc build

## Timezone
```
export TZ="Europe/London"
sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 
sudo vi /etc/timezone
```

add your timezone

## base packages
```
sudo apt-get update && sudo apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        libssl-dev \
        wget \
        tzdata \
        sudo \
        software-properties-common \
        python3 python3-dev python3-pip python3-venv \
        libsasl2-dev \
        git \
        openssh-server
```
let it start whatever     


## upgrade pip and get spacy
pip install --upgrade pip
pip install --upgrade pip pipenv
pip install spacy
python3 -m spacy download en_core_web_md
python3 -m spacy download en_core_web_lg

## Install HF CLI tool
export HFVER=1.28.1
sudo wget https://github.com/zia-ai/humanfirst/releases/download/cli-$HFVER/hf-linux-amd64?raw=true -O /usr/local/bin/hf 
sudo chmod 755 /usr/local/bin/hf

## Format source volume
DONT DO THIS EACH TIME! sudo mkfs -t ext4 /dev/xvdf

## mount source
```
lsblk -o NAME,FSTYPE,UUID,MOUNTPOINTS
mkdir /home/ubuntu/source
sudo vi /etc/fstab
UUID=0490832d-e7bf-4f44-bd70-667c51726aae  /home/ubuntu/source ext4 defaults 0 0
```

MAKE SURE YOU VERIFY IT BEFORE REBOOT
```
sudo findmnt --verify
```

## reboot
sudo reboot

## make all the files yours
sudo chown -R ubuntu:ubuntu /home/ubuntu/source

## setup github
* tj-workbench          (bitbucket - not using)
* project-williamsville (bitbucket - for your code)
* academy               (github hf - for examples to do with humanfirst)
* tj-ca                 (codecommit - for examples to do with previous content analytics work)

all of these are going to work off one key

## setup SSH keys

check ssh runnin
```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```


COPY .bashrc_custom /home/ubuntu/.bashrc
