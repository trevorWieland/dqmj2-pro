#include "context.h"
GT2Bool native_main_020b4134(GT2Connection connection, gsi_time now)
{
	if(connection->state < GTI2Connected)
	{
		GT2Bool timedOut = GT2False;
		if(connection->initiated)
		{
			if(connection->timeout)
			{
				if((now - connection->startTime) > connection->timeout)
					timedOut = GT2True;
			}
		}
		else
		{
			if(connection->state < GTI2AwaitingAcceptReject)
			{
				if((now - connection->startTime) > GTI2_SERVER_TIMEOUT)
					timedOut = GT2True;
			}
		}
		if(timedOut)
		{
			native_fn_020b589c(connection);
			native_fn_020b42a4(connection);
			if(!native_fn_020b3ca4(connection, GT2TimedOut, NULL, 0))
				return GT2False;
		}
	}
	return GT2True;
}
