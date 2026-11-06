#include "context.h"
GT2Bool native_main_020b41d8(GT2Connection connection, gsi_time now)
{
	if(!connection->pendingAck)
		return GT2True;
	if((now - connection->pendingAckTime) > GTI2_PENDING_ACK_TIME)
	{
		if(!native_fn_020b57a0(connection))
			return GT2False;
	}
	return GT2True;
}
