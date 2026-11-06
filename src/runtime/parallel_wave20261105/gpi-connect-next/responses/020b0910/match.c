#include "context.h"
GPResult
native_main_020b0910(
  GPConnection * connection,
  GPIOperation * operation,
  const char * input
)
{
	char buffer[16];
	int pid;
	GPICallback callback;

	
	
	if(gpiCheckForError(connection, input, GPITrue))
		return GP_SERVER_ERROR;

	
	
	if(strncmp(input, native_data_020e10d4, 5) != 0)
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_PARSE, native_data_020e10dc);

	
	
	if(!gpiValueForKey(input, native_data_020e110c, buffer, sizeof(buffer)))
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_PARSE, native_data_020e10dc);
	pid = atoi(buffer);

	
	
	callback = operation->callback;
	if(callback.callback != NULL)
	{
		GPNewProfileResponseArg * arg;
		arg = (GPNewProfileResponseArg *)gsimalloc(sizeof(GPNewProfileResponseArg));
		if(arg == NULL)
			Error(connection, GP_MEMORY_ERROR, native_data_020e1118);
		
		arg->profile = (GPProfile)pid;
		arg->result = GP_NO_ERROR;

		CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
	}

	
	
	gpiRemoveOperation(connection, operation);

	return GP_NO_ERROR;
}