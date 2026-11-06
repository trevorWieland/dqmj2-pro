#include "context.h"
GT2Bool native_main_020b45dc(GT2Connection connection, GT2Result result, GT2CloseReason reason)
{
	if(connection->state < GTI2Connected)
	{
		if(connection->initiated)
		{
			native_fn_020b42a4(connection);
			if(!native_fn_020b3ca4(connection, result, NULL, 0))
				return GT2False;
		}
		else
		{
			if(connection->state == GTI2AwaitingAcceptReject)
				connection->freeAtAcceptReject = GT2True;
			native_fn_020b42a4(connection);
		}
	}
	else if(connection->state != GTI2Closed)
	{
		native_fn_020b42a4(connection);
		if(!native_fn_020b3d60(connection, reason))
			return GT2False;
	}
	return GT2True;
}
