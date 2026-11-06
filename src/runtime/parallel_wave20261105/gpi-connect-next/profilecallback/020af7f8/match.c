#include "context.h"
GPResult
native_main_020af7f8(
  GPConnection * connection,
  const GPIOperation * operation
)
{
	GPICallback callback;
	GPIConnection * iconnection = (GPIConnection*)*connection;

	assert(connection != NULL);
	assert(*connection != NULL);
	assert(operation != NULL);

	callback = operation->callback;
	if(callback.callback != NULL)
	{
		
		
		switch(operation->type)
		{
		case GPI_CONNECT:
		{
			GPConnectResponseArg * arg;
			arg = (GPConnectResponseArg *)gsimalloc(sizeof(GPConnectResponseArg));
			if(arg == NULL)
				Error(connection, GP_MEMORY_ERROR, native_data_020e0f9c);
			memset(arg, 0, sizeof(GPConnectResponseArg));
			arg->result = operation->result;
			if(iconnection->errorCode == GP_NEWUSER_BAD_NICK)
			{
				arg->profile = (GPProfile)iconnection->profileid;
				iconnection->profileid = 0;
			}
			CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
			break;
		}
		case GPI_NEW_PROFILE:
		{
			GPNewProfileResponseArg * arg;
			arg = (GPNewProfileResponseArg *)gsimalloc(sizeof(GPNewProfileResponseArg));
			if(arg == NULL)
				Error(connection, GP_MEMORY_ERROR, native_data_020e0f9c);
			memset(arg, 0, sizeof(GPNewProfileResponseArg));
			arg->result = operation->result;
			CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
			break;
		}
		case GPI_DELETE_PROFILE:
		{
			GPDeleteProfileResponseArg * arg;
			arg = (GPDeleteProfileResponseArg *)gsimalloc(sizeof(GPDeleteProfileResponseArg));
			if (arg == NULL)
				Error(connection, GP_MEMORY_ERROR, native_data_020e0f9c);
			memset(arg, 0, sizeof(GPDeleteProfileResponseArg));
			arg->result = operation->result;
			CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
			break;

		}
		case GPI_GET_INFO:
		{
			GPGetInfoResponseArg * arg;
			arg = (GPGetInfoResponseArg *)gsimalloc(sizeof(GPGetInfoResponseArg));
			if(arg == NULL)
				Error(connection, GP_MEMORY_ERROR, native_data_020e0f9c);
			memset(arg, 0, sizeof(GPGetInfoResponseArg));
			arg->result = operation->result;
			CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
			break;
		}
		case GPI_PROFILE_SEARCH:
		{
			GPProfileSearchResponseArg * arg;
			arg = (GPProfileSearchResponseArg *)gsimalloc(sizeof(GPProfileSearchResponseArg));
			if(arg == NULL)
				Error(connection, GP_MEMORY_ERROR, native_data_020e0f9c);
			memset(arg, 0, sizeof(GPProfileSearchResponseArg));
			arg->result = operation->result;
			((GPProfileSearchResponseArg *)arg)->matches = NULL;
			CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
			break;
		}
		case GPI_REGISTER_UNIQUENICK:
		{
			GPRegisterUniqueNickResponseArg * arg;
			arg = (GPRegisterUniqueNickResponseArg *)gsimalloc(sizeof(GPRegisterUniqueNickResponseArg));
			if(arg == NULL)
				Error(connection, GP_MEMORY_ERROR, native_data_020e0f9c);
			memset(arg, 0, sizeof(GPRegisterUniqueNickResponseArg));
			arg->result = operation->result;
			CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
			break;
		}
		case GPI_REGISTER_CDKEY:
		{
			GPRegisterCdKeyResponseArg * arg;
			arg = (GPRegisterCdKeyResponseArg *)gsimalloc(sizeof(GPRegisterCdKeyResponseArg));
			if(arg == NULL)
				Error(connection, GP_MEMORY_ERROR, native_data_020e0f9c);
			memset(arg, 0, sizeof(GPRegisterCdKeyResponseArg));
			arg->result = operation->result;
			CHECK_RESULT(gpiAddCallback(connection, callback, arg, operation, 0));
			break;
		}
		default:
			assert(0);
		}
	}

	return GP_NO_ERROR;
}