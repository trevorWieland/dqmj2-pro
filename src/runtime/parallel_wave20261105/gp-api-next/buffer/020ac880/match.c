#include "context.h"
GPResult
native_main_020ac880(
  GPConnection * connection,
  SOCKET sock,
  GPIBuffer * inputBuffer,
  int * bytesRead,
  GPIBool * connClosed,
  char id[3]
)
{
	char * buffer;
	int len;
	int size;
	int rcode;
	int total;
	GPIBool closed;

	assert(sock != INVALID_SOCKET);
	assert(inputBuffer != NULL);
	assert(bytesRead != NULL);
	assert(connClosed != NULL);

	
	
	buffer = inputBuffer->buffer;
	len = inputBuffer->len;
	size = inputBuffer->size;
	total = 0;
	closed = GPIFalse;

	do
	{
		
		
		if((len + GPI_READ_SIZE) > size)
		{
			size = (len + GPI_READ_SIZE);
			buffer = (char *)gsirealloc(buffer, (unsigned int)size + 1);
			if(buffer == NULL)
				Error(connection, GP_MEMORY_ERROR, native_data_020e07c4);
            inputBuffer->size = size;
            inputBuffer->buffer = buffer;
		}

		
		rcode = recv(sock, &buffer[len], size - len, 0);


		if(gsiSocketIsError(rcode))
		{
			int error = GOAGetLastError(sock);
			if((error != WSAEWOULDBLOCK) && (error != WSAEINPROGRESS) && (error != WSAETIMEDOUT) )
			{
				Error(connection, GP_NETWORK_ERROR, native_data_020e0800);
			}
		}
		else if(rcode == 0)
		{
			
			
			closed = GPITrue;
			gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_Comment,
				"RECVXXXX(%s): Connection closed\n", id);
		}
		else
		{
			#if defined(GPI_DUMP_NET_TRAFFIC) && defined(GSI_COMMON_DEBUG)
			{
				static int recvCount;
				char *buf = (char *)gsimalloc((size_t)(rcode + 1));
				memcpy(buf, &buffer[len], (size_t)rcode);
				buf[rcode] = '\0';
				gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_RawDump,
					"RECV%04d(%s): %s\n", recvCount++, id, buf);
				freeclear(buf);
			}
			#elif defined(GSI_COMMON_DEBUG)
			{
				static int recvCount;
				gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_RawDump,
					"RECV%04d(%s): %d\n", recvCount++, id, rcode);
			}
			#endif
			
			
			len += rcode;

			
			
			total += rcode;
		}

		buffer[len] = '\0';
	}
	while((rcode >= 0) && !closed && (total < (128 * 1024)));

	if(total)
	{
		gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_RawDump,
			"RECVTOTL(%s): %d\n", id, total);
	}
	
	
	
	inputBuffer->buffer = buffer;
	inputBuffer->len = len;
	inputBuffer->size = size;
	*bytesRead = total;
	*connClosed = closed;

	GSI_UNUSED(id); 

	return GP_NO_ERROR;
}
