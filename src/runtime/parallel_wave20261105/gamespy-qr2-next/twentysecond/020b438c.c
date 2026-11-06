#include "context.h"
GT2Result native_main_020b438c
(
	GT2Socket socket,
	GT2Connection * connection,
	const char * remoteAddress,
	const GT2Byte * message,
	int len,
	int timeout,
	GT2ConnectionCallbacks * callbacks,
	GT2Bool blocking
)
{
	GT2Connection connectionTemp;
	GT2Result result;
	GT2Bool done;
	unsigned int ip;
	unsigned short port;
	{
		if(!native_fn_020b5fac(remoteAddress, &ip, &port) || !ip || !port)
			return GT2AddressError;
	}
	if((ntohl(ip) & GTI2_INVALID_IP_MASK) == GTI2_INVALID_IP_MASK)
		return GT2AddressError;
	result = native_fn_020b3ff4(socket, &connectionTemp, ip, port);
	if(result)
		return result;
	connectionTemp->timeout = (unsigned int)timeout;
	result = native_fn_020b402c(connectionTemp, message, len, callbacks);
	if(result)
	{
		native_fn_020b5cd0(connectionTemp);
		return result;
	}
	if(!blocking)
	{
		if(connection)
			*connection = connectionTemp;
		return GT2Success;
	}
	connectionTemp->callbackLevel++;
	do
	{
		native_fn_020b4354(socket);
		done = (connectionTemp->state >= GTI2Connected);
		if(!done)
			native_fn_020a8f14(1);
	} while(!done);
	connectionTemp->callbackLevel--;
	if(connectionTemp->state == GTI2Connected)
		*connection = connectionTemp;
	return connectionTemp->connectionResult;
}
