#include "context.h"
int native_main_020b30c8(void)
{
	int len;
	int processed;

	if (sock == INVALID_SOCKET)
		return 0;

	if (stats_initstate != init_complete)
		return 0;

	while (SocketReadable(sock))
	{
		if (rcvmax - rcvlen < 128) 
		{
			if (rcvmax < 256)
				rcvmax = 256;
			else
				rcvmax *= 2;
			rcvbuffer = gsirealloc(rcvbuffer, (unsigned int)(rcvmax+1));
			if (rcvbuffer == NULL)
				return 0; 
		}
		len = recv(sock, rcvbuffer + rcvlen, rcvmax - rcvlen, 0);		
		if (len <= 0) 
		{
			CloseStatsConnection();
			return 0;
		}
		rcvlen += len;
		rcvbuffer[rcvlen] = 0;

		processed = ProcessInBuffer(rcvbuffer, rcvlen);
		if (processed == rcvlen) 
			rcvlen = 0;
		else
		{
			
			memmove(rcvbuffer,rcvbuffer + processed, (unsigned int)(rcvlen - processed));
			rcvlen -= processed;
		}
		
		
	}
	if (sock == INVALID_SOCKET)
		return 0;
	else
		return 1;

}
