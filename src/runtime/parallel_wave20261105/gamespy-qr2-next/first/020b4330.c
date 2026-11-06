#include "context.h"
GT2Result native_main_020b4330
(
	GT2Socket * socket,
	const char * localAddress,
	int outgoingBufferSize,
	int incomingBufferSize,
	gt2SocketErrorCallback callback
)
{
	return native_fn_020b59d4(socket, localAddress, outgoingBufferSize, incomingBufferSize, callback, GTI2UdpProtocol);
}
