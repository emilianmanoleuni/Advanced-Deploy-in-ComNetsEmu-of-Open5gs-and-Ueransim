echo "----------------------------"
echo "Initializing $COMPONENT_NAME"
echo "----------------------------"

STATUS_FILE_GNB="${STATUS_DIR_PATH}/ueransim_gnb_status.txt"

echo "starting" > $STATUS_FILE

#apt update && apt install net-tools

echo "ready" > $STATUS_FILE

echo "----------------------------"
echo "Waiting GNB to be avaible"
echo "----------------------------"

while true; do
    if [ -f "$STATUS_FILE_GNB" ]; then
        STATUS=$(cat "$STATUS_FILE_GNB")
        if [ "$STATUS" == "avaible" ]; then
            break
        fi
    else
       echo "Status file cant't be found"
    fi
done

sleep 10

./entrypoint.sh ue -n 5
