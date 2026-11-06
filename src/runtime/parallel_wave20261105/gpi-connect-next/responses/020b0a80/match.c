#include "context.h"
GPResult
native_main_020b0a80
(
  GPConnection * connection,
  GPIOperation * operation,
  const char * input
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPICallback callback;

	
	
	if(gpiCheckForError(connection, input, GPITrue))
		return GP_SERVER_ERROR;

	
	
	if(strncmp(input, native_data_020e1128, 5) != 0)
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_PARSE, native_data_020e10dc);

	
	
	
	callback = operation->callback;
	if(callback.callback != NULL)
	{
		GPDeleteProfileResponseArg * arg;
		arg = (GPDeleteProfileResponseArg *)gsimalloc(sizeof(GPDeleteProfileResponseArg));
		if(arg == NULL)
			Error(connection, GP_MEMORY_ERROR, native_data_020e1118);
		
		arg->profile = iconnection->profileid;
		arg->result = GP_NO_ERROR;

		CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
	}

	
	
	gpiRemoveOperation(connection, operation);

	return GP_NO_ERROR;
}