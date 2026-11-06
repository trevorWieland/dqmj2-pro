#include "context.h"
GT2Bool native_main_020b4a00(GT2Connection connection)
{
	GT2Bool localClose;
	if(!native_fn_020b589c(connection))
		return GT2False;
	localClose = (connection->state == GTI2Closing);
	if(!native_fn_020b45dc(connection, GT2Rejected, localClose?GT2LocalClose:GT2RemoteClose))
		return GT2False;
	return GT2True;
}
