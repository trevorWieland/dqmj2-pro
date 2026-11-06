#include "context.h"
GT2Bool native_main_020b4204(GT2Connection connection, gsi_time now)
{
	if((now - connection->lastSend) > GTI2_KEEP_ALIVE_TIME)
	{
		if(!native_fn_020b56a8(connection))
			return GT2False;
	}
	return GT2True;
}
