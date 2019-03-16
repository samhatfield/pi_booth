#/bin/bash

# Configuration
USERNAME=pi
REMOTE=head.local
DIR=/mnt/autumn/openifs-cy38r1/run
EXPID=h467

# Counter for time steps
NUM=000000

# Final time step to copy
FINAL=002350

download_gg=false

while [ 1 ]
do
    if [ "$NUM" = "$FINAL" ]; then
        echo "Finished"
        exit 0
    fi

    # Download file if it exists
    if ssh -t $USERNAME@$REMOTE "[ -f $DIR/ICMSH$EXPID+$NUM ]"
    then
        echo "Downloading $NUM"
        scp $USERNAME@$REMOTE:$DIR/ICMSH$EXPID+$NUM .
        if [ "$download_gg" = true ]; then
            scp $USERNAME@$REMOTE:$DIR/ICMGG$EXPID+$NUM .
        fi

        # Convert to NetCDF
        grib_copy ICMSH$EXPID+$NUM ICMSH$EXPID+${NUM}_[typeOfLevel]
        cdo -t ecmwf -f nc copy -sp2gpl ICMSH$EXPID+${NUM}_isobaricInhPa ICMSH$EXPID+$NUM.nc
        rm ICMSH$EXPID+$NUM ICMSH$EXPID+${NUM}_isobaricInhPa

        if [ "$download_gg" = true ]; then
            cdo -R copy ICMGG$EXPID+$NUM ICMGG$EXPID+${NUM}_2
            grib_to_netcdf -o ICMGG$EXPID+$NUM.nc ICMGG$EXPID+${NUM}_2
            rm ICMGG$EXPID+$NUM ICMGG$EXPID+${NUM}_2
        fi

        NUM=$(printf %06d "$((10#$NUM + 1))")
    # Else sleep for a second
    else
        echo "ICMSH$EXPID+$NUM doesn't exist"
        sleep 1
    fi
done
