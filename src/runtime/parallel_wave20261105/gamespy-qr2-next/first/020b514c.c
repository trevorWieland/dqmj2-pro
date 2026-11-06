#include "context.h"
GT2Bool native_main_020b514c(GT2Socket socket, unsigned int ip, unsigned short port)
{
	GT2Connection connection;
	connection = native_fn_020b59ac(socket, ip, port);
	if(socket->receiveDumpCallback)
	{
		if(!native_fn_020b3f00(socket, connection, ip, port, GT2True, NULL, 0, GT2False))
			return GT2False;
	}
	if(!connection)
		return GT2True;
	if(connection->state == GTI2AwaitingServerChallenge)
	{
		if(!connection->timeout || ((native_fn_020a8ef8() - connection->startTime) < connection->timeout))
			return GT2True;
		if(!native_fn_020b45dc(connection, GT2TimedOut, GT2RemoteClose))
			return GT2False;
	}
	else
	{
		if(!native_fn_020b45dc(connection, GT2Rejected, GT2RemoteClose))
			return GT2False;
	}
	return GT2True;
}
