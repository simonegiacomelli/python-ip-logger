while [ true ]; do
    git pull
    python3 main.py 2>&1 | tee -a reboot.log
done