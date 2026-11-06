#include "context.h"
GPResult
native_main_020af244(
  GPConnection * connection,
  GPProfile profile, 
  GPEnum checkCache,
  GPEnum blocking,
  GPCallback callback,
  void * param
)
{
	GPIProfile * pProfile;
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIOperation * operation = NULL;
	GPIBool useCache;
	GPResult result;
	int id;

	
	
	useCache = (checkCache == GP_CHECK_CACHE) ? GPITrue:GPIFalse;

	
	
	if(!iconnection->infoCaching)
		useCache = GPIFalse;

	
	
	if(callback && useCache && gpiGetProfile(connection, profile, &pProfile) && pProfile->cache)
	{
		GPICallback gpiCallback;
		GPGetInfoResponseArg * arg;

		arg = (GPGetInfoResponseArg *)gsimalloc(sizeof(GPGetInfoResponseArg));
		if(arg == NULL)
			Error(connection, GP_MEMORY_ERROR, native_data_020e0db8);

		gpiInfoCacheToArg(pProfile->cache, arg);
		arg->result = GP_NO_ERROR;
		arg->profile = profile;
		
		gpiCallback.callback = callback;
		gpiCallback.param = param;

		
		
		CHECK_RESULT(gpiAddOperation(connection, GPI_GET_INFO, NULL, &operation, GP_BLOCKING, callback, param));
		id = operation->id;

		
		
		CHECK_RESULT(gpiAddCallback(connection, gpiCallback, arg, operation, 0));

		
		
		gpiRemoveOperation(connection, operation);
	}
	else
	{
		
		
		CHECK_RESULT(gpiAddOperation(connection, GPI_GET_INFO, NULL, &operation, blocking, callback, param));
		id = operation->id;

		
		
		result = gpiSendGetInfo(connection, profile, operation->id);
		CHECK_RESULT(result);
	}

	
	
	if(blocking)
	{
		result = gpiProcess(connection, id);
		CHECK_RESULT(result);
	}

	return GP_NO_ERROR;
}