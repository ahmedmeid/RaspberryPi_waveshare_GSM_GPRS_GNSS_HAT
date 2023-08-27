#!/bin/bash

# Run the main script in a loop with a 3-second delay
for ((i=0; i<4; i++)); do
    /home/pi/Dev/test_socket.py
    sleep 3
done
