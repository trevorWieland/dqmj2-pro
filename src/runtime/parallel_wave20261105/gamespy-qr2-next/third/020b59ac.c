#include "context.h"
GT2Connection native_main_020b59ac(GT2Socket socket, unsigned int ip, unsigned short port)
{
	GTI2Connection connection;
	GT2Connection connectionPtr;
	GT2Connection * connectionPtrPtr;
	connection.ip = ip;
	connection.port = port;
	connectionPtr = &connection;
	connectionPtrPtr = (GT2Connection *)native_fn_020a8a3c(socket->connections, &connectionPtr);
	if(connectionPtrPtr)
		return *connectionPtrPtr;
	return NULL;
}
