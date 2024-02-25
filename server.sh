#!/bin/bash

rm -f response
mkfifo response

PORT=8080

function handle_req() {
	READING_BODY=0
	BODY=""
	ERROR=0
	
	while read raw_line; do
		line=`echo $raw_line | tr -d ['\r\n']`

		if [ -z "$line" ]; then
			if [ $READING_BODY == 0 ]; then
				READING_BODY=1
				continue
			else
				break
			fi
		fi

		if [ $READING_BODY == 0 ]; then
			# Reading header
			HEADLINE_REGEX='.* /api/partners.*'

			if [[ "$line" =~ $HEADLINE_REGEX ]]; then
                                arr=($line)
                                REQUEST="${arr[@]:0:2}"
			fi
		else
			# Reading body
			
			BODY="$BODY$line\r\n"
		fi
	done

	BODY=$(echo -e "$BODY" | tr -d '\r\n')

	echo REQ: --$REQUEST--

	if [[ "$REQUEST" =~ ^POST\ /api/partners$ ]]; then
			 DATA=$(python3 relay.py 0 $BODY)
	elif [[ "$REQUEST" =~ ^GET\ /api/partners/[0-9]+$ ]]; then
			 DATA=$(python3 relay.py 1 $REQUEST $BODY)
	elif [[ "$REQUEST" =~ ^PUT\ /api/partners/[0-9]+/cashback$ ]]; then
			 DATA=$(python3 relay.py 2 $REQUEST $BODY)
	else
		 ERROR=1
	fi


	RESPONSE="HTTP/1.1 200 OK\r\n\r\n$DATA"

	if [ $ERROR == 1 ]; then
		RESPONSE=$(cat 400.html)
	fi

	if [ "$DATA" == "-1" ]; then
		RESPONSE=$(cat 404.html)
	fi

	echo $RESPONSE
	echo "$RESPONSE" > response

}

echo Listening on port $PORT

while true; do
	cat response | nc -lv 8080 | handle_req
done
