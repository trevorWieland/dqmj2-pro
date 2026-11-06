#include "context.h"
GT2Bool native_main_020b523c(GT2Socket socket)
{
	int rcode;
	SOCKADDR_IN address;
	int addressLen;
	#if (GTI2_STACK_RECV_BUFFER_SIZE > 1600)
		static char buffer[GTI2_STACK_RECV_BUFFER_SIZE];
	#else
		char buffer[GTI2_STACK_RECV_BUFFER_SIZE];
	#endif
	#ifdef GSI_ADHOC
	if(socket->protocolType == GTI2AdHocProtocol)
	{
		return gti2ReceiveAdHocMessages(socket,buffer,GTI2_STACK_RECV_BUFFER_SIZE);
	}
	#endif
	while	(native_fn_020a8d88(socket->socket))
	{
		addressLen = sizeof(address);
		rcode = native_fn_020a8c00(socket->socket, buffer, sizeof(buffer), 0, (SOCKADDR *)&address, &addressLen);
		if (gsiSocketIsError(rcode))
		{
			rcode = native_fn_020a8c9c(socket->socket);
			if(rcode == WSAECONNRESET)
			{
				if(!native_fn_020b514c(socket, address.sin_addr.s_addr, ntohs(address.sin_port)))
					return GT2False;
			}
			#ifndef SN_SYSTEMS
				else if (rcode == WSAEHOSTUNREACH)
				{
					if (!native_fn_020b51dc(socket, address.sin_addr.s_addr, ntohs(address.sin_port), GT2False))
						return GT2False;
				}
			#endif
			else if(rcode != WSAEMSGSIZE)
			{
				native_fn_020b5f14(socket);
				return GT2False;
			}
		}
		else
		{
			#ifdef RECV_LOG
				gti2LogMessage(address.sin_addr.s_addr, ntohs(address.sin_port),
					socket->ip, socket->port,
					buffer, rcode);
			#endif
			if(!native_fn_020b4f80(socket, (GT2Byte *)buffer, rcode, address.sin_addr.s_addr, ntohs(address.sin_port)))
				return GT2False;
		}
	}
	return GT2True;
}
