#include "context.h"
GPResult
native_main_020afa1c(
  GPConnection * connection,
  int type,
  void * data,
  GPIOperation ** op,
  GPEnum blocking,
  GPCallback callback,
  void * param
)
{
	GPIOperation * operation;
	GPIConnection * iconnection = (GPIConnection*)*connection;

	
	
	operation = (GPIOperation *)gsimalloc(sizeof(GPIOperation));
	if(operation == NULL)
		Error(connection, GP_MEMORY_ERROR, native_data_020e0f9c);

	
	
	operation->type = type;
	operation->data = data;
	operation->blocking = (GPIBool)blocking;
	operation->state = GPI_START;
	if(type == GPI_CONNECT)
	{
		
		
		operation->id = 1;
	}
	else
	{
		operation->id = iconnection->nextOperationID++;
		if(iconnection->nextOperationID < 2)
			iconnection->nextOperationID = 2;
	}
	operation->result = GP_NO_ERROR;
	operation->callback.callback = callback;
	operation->callback.param = param;

	
	
	operation->pnext = iconnection->operationList;
	iconnection->operationList = operation;

	*op = operation;
	return GP_NO_ERROR;
}
