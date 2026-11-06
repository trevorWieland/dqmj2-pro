#include "context.h"
int native_main_020b5e8c(void * elem, void * clientData)
{
	GT2Connection connection = *(GT2Connection *)elem;
	gsi_time now = *(gsi_time *)clientData;
	if(connection->state != GTI2Closed)
	{
		if(!native_fn_020b4228(connection, now))
			return 0;
	}
	if((connection->state == GTI2Closed) && !connection->freeAtAcceptReject && !connection->callbackLevel)
		native_fn_020b5cd0(connection);
	return 1;
}
