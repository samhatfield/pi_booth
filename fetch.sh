#/bin/bash

# Configuration
USERNAME=pi
REMOTE=head.local
DIR=/mnt/autumn/openifs-cy38r1/run
EXPID=h3b6

# Counter for time steps
NUM=000000

# Final time step to copy
FINAL=000120

while [ 1 ]
do
    if [ "$NUM" = "$FINAL" ]; then
        echo "Finished"
        exit 0
    fi

    # Download file if it exists
    if ssh -t $USERNAME@$REMOTE "[ -f $DIR/ICMSH$EXPID+$NUM ]"
    then
        echo "Downloading ICMSH$EXPID+$NUM"
        scp $USERNAME@$REMOTE:$DIR/ICMSH$EXPID+$NUM .

        # Convert to NetCDF
        grib_copy ICMSH$EXPID+$NUM ICMSH$EXPID+${NUM}_[typeOfLevel]
        cdo -t ecmwf -f nc copy -sp2gpl ICMSHh3b6+${NUM}_isobaricInhPa ICMSHh3b6+$NUM.nc
        NUM=$(printf %06d "$((10#$NUM + 1))")
    # Else sleep for a second
    else
        echo "ICMSH$EXPID+$NUM doesn't exist"
        sleep 1
    fi
done
