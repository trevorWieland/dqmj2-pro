#include "context.h"
GT2Bool native_main_020b49b8(GT2Connection connection, GT2Byte * message, int len)
{
	if(connection->state != GTI2AwaitingAcceptance)
	{
		if(!native_fn_020b4634(connection))
			return GT2False;
		return GT2True;
	}
	native_fn_020b42a4(connection);
	if(!native_fn_020b589c(connection))
		return GT2False;
	if(!native_fn_020b3ca4(connection, GT2Rejected, message, len))
		return GT2False;
	return GT2True;
}
