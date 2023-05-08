#!/bin/bash
sshpass -p 'sanjiang666' ssh -p 2201  root@193.0.30.240 "cd /opt/search-enginer-ai && git pull"

sshpass -p 'sanjiang666' ssh -p 2201  root@193.0.30.240 "cd /opt/search-enginer-ai && git pull"

sshpass -p 'sanjiang666' ssh -p 2201  root@193.0.30.240 "cd /opt/search-enginer-ai && conda deactivate  && conda activate aise37 && python goods_ai_app_server.py"

sshpass -p 'sanjiang666' ssh -p 2201  root@193.0.30.240 "cd /opt && git clone https://gitlab+deploy-token-2:g8bKiryU8sovKauDdKhy@gitlab.sanjiang.com:it-group/search-enginer-ai.git"

git clone https://gitlab+deploy-token-2:g8bKiryU8sovKauDdKhy@gitlab.sanjiang.com/it-group/search-enginer-ai.git


git@gitlab.sanjiang.com:it-group/search-enginer-ai.git


export PATH="/root/anaconda3/envs/aise37/bin:$PATH"