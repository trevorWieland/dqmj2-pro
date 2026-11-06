#include "context.h"
void native_main_020b5cd0(GT2Connection connection)
{
	if(connection->freeAtAcceptReject || connection->callbackLevel)
		return;
	if(connection->state == GTI2Closed)
	{
		int len;
		int i;
		len = native_fn_020a8640(connection->socket->closedConnections);
		for(i = 0 ; i < len ; i++)
		{
			if(connection == *(GT2Connection *)native_fn_020a8644(connection->socket->closedConnections, i))
			{
				native_fn_020a8720(connection->socket->closedConnections, i);
				return;
			}
		}
	}
	else
	{
		native_fn_020a89f0(connection->socket->connections, &connection);
	}
}
