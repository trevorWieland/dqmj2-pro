#include "context.h"
void native_main_020b4270(GT2Connection connection, GT2Bool hard)
{
	if(hard)
	{
		if(connection->state >= GTI2Closed)
			return;
		native_fn_020b42a4(connection);
		native_fn_020b589c(connection);
		native_fn_020b3d60(connection, GT2LocalClose);
		native_fn_020b5cd0(connection);
	}
	else
	{
		connection->state = GTI2Closing;
		native_fn_020b5668(connection);
	}
}
