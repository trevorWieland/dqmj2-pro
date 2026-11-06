#include "context.h"
void native_main_020b40d8(GT2Connection connection, const GT2Byte * message, int len)
{
	
	connection->freeAtAcceptReject = GT2False;

	
	if(connection->state != GTI2AwaitingAcceptReject)
		return;

	
	gti2MessageCheck(&message, &len);

	
	gti2SendReject(connection, message, len);

	
	connection->state = GTI2Closing;
}
