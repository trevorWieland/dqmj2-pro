#include "context.h"
GPResult native_main_020b29a0(
  GPConnection * connection,
  GPIOperation * operation,
  const char * input
)
{
	GPICallback callback;

	
	
	if(gpiCheckForError(connection, input, GPITrue))
		return GP_SERVER_ERROR;

	
	
	if(strncmp(input, native_data_020e157c, 4) != 0)
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_PARSE, native_data_020e153c);

	
	
	callback = operation->callback;
	if(callback.callback != NULL)
	{
		GPRegisterCdKeyResponseArg * arg;
		arg = (GPRegisterCdKeyResponseArg *)gsimalloc(sizeof(GPRegisterCdKeyResponseArg));
		if(arg == NULL)
			Error(connection, GP_MEMORY_ERROR, native_data_020e156c);

		arg->result = GP_NO_ERROR;

		CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
	}

	
	
	gpiRemoveOperation(connection, operation);

	return GP_NO_ERROR;
}
