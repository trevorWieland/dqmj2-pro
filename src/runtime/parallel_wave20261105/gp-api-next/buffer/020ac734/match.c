#include "context.h"
GPResult
native_main_020ac734(
  GPConnection * connection,
  SOCKET sock,
  const char * buffer,
  int bufferLen,
  GPIBool * closed,
  int * sent,
  char id[3]
)
{
	int rcode;

	rcode = send(sock, buffer, bufferLen, 0);
	if(gsiSocketIsError(rcode))
	{
		rcode = GOAGetLastError(sock);
		if((rcode != WSAEWOULDBLOCK) && (rcode != WSAEINPROGRESS) && (rcode != WSAETIMEDOUT) )
		{
			
			if((id[0] == 'P') && (id[1] == 'R'))
				return GP_NETWORK_ERROR;
			CallbackError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e07d8);
		}

		*sent = 0;
		*closed = GPIFalse;
	}
	else if(rcode == 0)
	{
		gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_Comment,
			"SENDXXXX(%s): Connection closed\n", id);

		*sent = 0;
		*closed = GPITrue;
	}
	else
	{
		#if defined(GPI_DUMP_NET_TRAFFIC) && defined(GSI_COMMON_DEBUG)
		{
			static int sendCount;
			char *buf = (char *)gsimalloc((size_t)(rcode + 1));
			memcpy(buf, buffer, (size_t)rcode);
			buf[rcode] = '\0';
			gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_RawDump, "SENT%04d(%s): %s\n", sendCount++, id, buf);
			freeclear(buf);
		}
		#elif defined(GSI_COMMON_DEBUG)
		{
			static int sendCount;
			gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_RawDump,
				"SENT%04d(%s): %d\n", sendCount++, id, rcode);
		}
		#endif

		*sent = rcode;
		*closed = GPIFalse;
	}

	return GP_NO_ERROR;
}
