#include "context.h"
GPIPeer*
native_main_020b03c4(const GPConnection *connection,
                           unsigned int ip,
                           unsigned short port)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIPeer * pcurr;

	GS_ASSERT(ip);
	GS_ASSERT(port);
	if (!ip && !port)
		return NULL;
	
	
	for(pcurr = iconnection->peerList ; pcurr != NULL ; pcurr  = pcurr->pnext)
	{
		
		
		if(pcurr->ip == ip && pcurr->port == port)
		{
			
			
			return pcurr;
		}
	}

	return NULL;
}