#include "context.h"
GT2Bool native_main_020b409c(GT2Connection connection, GT2ConnectionCallbacks * callbacks)
{
	
	if(connection->freeAtAcceptReject)
	{
		
		connection->freeAtAcceptReject = GT2False;

		
		return GT2False;
	}

	
	connection->freeAtAcceptReject = GT2False;

	
	if(connection->state != GTI2AwaitingAcceptReject)
		return GT2False;

	
	gti2SendAccept(connection);

	
	connection->state = GTI2Connected;

	
	if(callbacks)
		connection->callbacks = *callbacks;

	return GT2True;
}
