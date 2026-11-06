#include "context.h"
void
native_main_020acbcc(
  GPConnection * connection,
  GPResult result,
  GPEnum fatal
)
{
	GPICallback callback;
	GPIConnection * iconnection = (GPIConnection*)*connection;

	assert(iconnection != NULL);
	assert(result != GP_NO_ERROR);
	assert((fatal == GP_FATAL) || (fatal == GP_NON_FATAL));

	if(fatal == GP_FATAL)
		iconnection->fatalError = GPITrue;

	callback = iconnection->callbacks[GPI_ERROR];
	if(callback.callback != NULL)
	{
		GPErrorArg * arg;
		arg = (GPErrorArg *)gsimalloc(sizeof(GPErrorArg));

		if(arg != NULL)
		{
			arg->result = result;
			arg->fatal = fatal;
			arg->errorCode = iconnection->errorCode;
#ifndef GSI_UNICODE
			arg->errorString = iconnection->errorString;
#else
			arg->errorString = iconnection->errorString_W;
#endif

		}

		gpiAddCallback(connection, callback, arg, NULL, GPI_ADD_ERROR);
	}
}
