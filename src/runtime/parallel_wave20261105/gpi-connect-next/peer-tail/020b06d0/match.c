#include "context.h"
void
native_main_020b06d0(unsigned int ip, unsigned short port, unsigned char *message, 
							unsigned int messageLength, gsi_bool reliable, void *userData)
{
	GPConnection *connection = (GPConnection *)userData;
	GPIPeer *aPeer;
	unsigned char * buff;
	int writePos;
	int size;
	IN_ADDR anAddr;
	anAddr.s_addr = ip;
	aPeer = gpiGetPeerByAddr(connection, ip, port);
	if (!aPeer)
	{
		aPeer = gpiAddPeer(connection, -1, GPIFalse);
		if (aPeer)
		{
			aPeer->state = GPI_PEER_WAITING;
			aPeer->ip = ip;
			aPeer->port = port;
		}
		else 
		{
			((void)0);
			return;
		}
	}

	buff = (unsigned char *)aPeer->inputBuffer.buffer;
	writePos = aPeer->inputBuffer.len;
	size = aPeer->inputBuffer.size;

	
	
	if((int)messageLength > (size - writePos))
	{
		unsigned char *reallocedBuff;
		size = (writePos + max(GPI_READ_SIZE,(int)messageLength));
		reallocedBuff = (unsigned char *)gsirealloc(buff, (unsigned int)size + 1);
		if(reallocedBuff == NULL)
		{
			((void)0);
			gsifree(buff);
			gpiSetErrorString(connection, native_data_020e104c);
			gpiCallErrorCallback(connection, GP_MEMORY_ERROR, GP_NON_FATAL);
			return;
		}
		else
			buff = reallocedBuff;
	}

	memcpy(&buff[writePos], message, messageLength);

	aPeer->inputBuffer.buffer = (char *)buff;
	aPeer->inputBuffer.len += messageLength;
	aPeer->inputBuffer.size = size;
	buff[aPeer->inputBuffer.len] = '\0';
	GSI_UNUSED(reliable);
	GSI_UNUSED(anAddr);
}