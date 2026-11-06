#include "context.h"
GPResult
native_main_020acc28(
  GPConnection * connection,
  GPICallback callback,
  void * arg,
  const struct GPIOperation_s * operation,
  int type
)
{
	GPICallbackData * data;
	GPIConnection * iconnection = (GPIConnection*)*connection;

	
	
	data = (GPICallbackData *)gsimalloc(sizeof(GPICallbackData));
	if(data == NULL)
		Error(connection, GP_MEMORY_ERROR, native_data_020e0840);
	data->callback = callback;
	data->arg = arg;
	if(operation != NULL)
		data->operationID = operation->id;
	else
		data->operationID = 0;
	data->type = type;
	data->pnext = NULL;

	
	
	if(iconnection->callbackList == NULL)
		iconnection->callbackList = data;
	if(iconnection->lastCallback != NULL)
		iconnection->lastCallback->pnext = data;
	iconnection->lastCallback = data;

	return GP_NO_ERROR;
}
