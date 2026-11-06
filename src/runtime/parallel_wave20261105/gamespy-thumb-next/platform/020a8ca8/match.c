#include "context.h"
int native_main_020a8ca8(SOCKET theSocket, int* theReadFlag, int* theWriteFlag, int* theExceptFlag)
{
	SOPollFD pollFD;
	int rcode;
	
	pollFD.fd = theSocket;
	pollFD.events = 0;
	if(theReadFlag != NULL)
		pollFD.events |= SOC_POLLRDNORM;
	if(theWriteFlag != NULL)
		pollFD.events |= SOC_POLLWRNORM;
	pollFD.revents = 0;

	rcode = native_fn_020907f4(&pollFD, 1, 0);
	if(rcode < 0)
		return NITRO_SOCKET_ERROR;

	if(theReadFlag != NULL)
	{
		if((rcode > 0) && (pollFD.revents & (SOC_POLLRDNORM|SOC_POLLHUP)))
			*theReadFlag = 1;
		else
			*theReadFlag = 0;
	}
	if(theWriteFlag != NULL)
	{
		if((rcode > 0) && (pollFD.revents & SOC_POLLWRNORM))
			*theWriteFlag = 1;
		else
			*theWriteFlag = 0;
	}
	if(theExceptFlag != NULL)
	{
		if((rcode > 0) && (pollFD.revents & SOC_POLLERR))
			*theExceptFlag = 1;
		else
			*theExceptFlag = 0;
	}
	return rcode;
}