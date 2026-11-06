#include "context.h"
GT2Bool native_main_020b475c(GT2Connection connection, GT2Byte * message, int len)
{
	if((connection->state != GTI2Connected) && (connection->state != GTI2Closing))
	{
		if(!native_fn_020b4634(connection))
			return GT2False;
	}
	else
	{
		if(native_fn_020a8640(connection->receiveFilters))
		{
			if(!native_fn_020b3e80(connection, 0, message, len, GT2True))
				return GT2False;
			return GT2True;
		}
		if(!native_fn_020b3d04(connection, message, len, GT2True))
			return GT2False;
	}
	return GT2True;
}
