#include "context.h"
GPResult native_main_020ac9e8(GPConnection * connection, unsigned int ip, unsigned short port, 
							 GPIBuffer * outputBuffer, GPIBool *closed, GPIBool clipSentData)
{
	GPIConnection *iconnection = (GPIConnection *)*connection;
	
	unsigned int remaining;
	unsigned char * buffer;
	unsigned int pos;
	unsigned int len;
	unsigned int total = 0;
	GSUdpPeerState aPeerState;
	assert(outputBuffer != NULL);

	buffer = (unsigned char *)outputBuffer->buffer;
	len = (unsigned int)outputBuffer->len;
	pos = (unsigned int)outputBuffer->pos;
	remaining = (len - pos);

	
	
	if(remaining == 0)
		return GP_NO_ERROR;

	
	
	if ((int)remaining <= (gsUdpEngineGetPeerOutBufferFreeSpace(ip, port) - GS_UDP_RELIABLE_MSG_HEADER - GS_UDP_MSG_HEADER_LEN))
	{
		gsUdpEngineSendMessage(ip, port, iconnection->mHeader, &buffer[pos], remaining, gsi_true);
		total = remaining;
		remaining = 0;
	}
	else
	{
		unsigned int freeSpace =0;
		unsigned int sendAmount = 0;
		do 
		{
			freeSpace = (unsigned int)gsUdpEngineGetPeerOutBufferFreeSpace(ip, port);
			sendAmount = freeSpace - (GS_UDP_MSG_HEADER_LEN + GS_UDP_RELIABLE_MSG_HEADER);
			if (sendAmount <= (GS_UDP_MSG_HEADER_LEN + GS_UDP_RELIABLE_MSG_HEADER))
				break;
			if (gsUdpEngineSendMessage(ip, port, iconnection->mHeader, &buffer[pos+total], sendAmount, gsi_true) == GS_UDP_SEND_FAILED)
				break;
			total += sendAmount;
			remaining -= sendAmount;
		}while (remaining);
	}

	if(clipSentData)
	{
		if (total > 0)
		{
			memmove(buffer, &buffer[total], remaining + 1);
			len -= total;
		}
	}
	else
	{
		pos += total;
	}
	
	
	outputBuffer->len = (int)len;
	outputBuffer->pos = (int)pos;

	gsUdpEngineGetPeerState(ip, port, &aPeerState);
	if (aPeerState == GS_UDP_PEER_CLOSED)
		*closed = GPITrue;
	else 
		*closed = GPIFalse;

	return GP_NO_ERROR;
}
