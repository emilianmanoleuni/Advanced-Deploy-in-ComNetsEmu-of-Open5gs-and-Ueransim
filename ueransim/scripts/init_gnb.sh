echo "----------------------------"
echo "Initializing $COMPONENT_NAME"
echo "----------------------------"

STATUS_FILE_AMF="${STATUS_DIR_PATH}/amf_status.txt"

echo "installing" > $STATUS_FILE
#apt update && apt install net-tools
echo "ready" > $STATUS_FILE

echo "----------------------------"
echo "Waiting AMF to be ready"
echo "----------------------------"

while true; do
    if [ -f "$STATUS_FILE_AMF" ]; then
        STATUS=$(cat "$STATUS_FILE_AMF")
        if [ "$STATUS" == "ready" ]; then
            break
        fi
    else
       echo "Status file cant't be found"
    fi
done

sleep 30


echo "avaible" > $STATUS_FILE

./entrypoint.sh gnb
