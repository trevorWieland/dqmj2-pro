#include "context.h"
void native_main_020b42a4(GT2Connection connection)
{
	if(connection->state == GTI2Closed)
		return;
	connection->state = GTI2Closed;
	native_fn_020a89f0(connection->socket->connections, &connection);
	native_fn_020a865c(connection->socket->closedConnections, &connection);
}
