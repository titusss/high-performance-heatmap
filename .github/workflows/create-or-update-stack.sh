set -e -x 
STACK_EXISTS=`openstack stack list |grep $STACK_NAME | wc -l`
if [ $STACK_EXISTS == 0 ]; then METHOD=create  ; else METHOD=update ; fi
openstack stack $METHOD -e $STACK_PARS -t $STACK_FILE $STACK_NAME -fjson
