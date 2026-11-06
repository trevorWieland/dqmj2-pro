#include "context.h"
GT2Bool native_main_020b4e8c(GT2Connection connection, const GT2Byte * message, int len)
{
	gsi_time startTime;
	if(!connection->callbacks.ping)
		return GT2True;
	if(len != (4 + sizeof(gsi_time)))
		return GT2True;
	if(native_fn_0201b248(message, native_data_020e170c, 4) != 0)
		return GT2True;
	memcpy(&startTime, message + 4, sizeof(gsi_time));
	if(!native_fn_020b3db0(connection, (int)(native_fn_020a8ef8() - startTime)))
		return GT2False;
	return GT2True;
}
