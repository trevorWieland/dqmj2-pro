#include "context.h"
GPResult native_main_020aa100(
  GPConnection * connection,
  GPProfile profile, 
  GPEnum checkCache,
  GPEnum blocking,
  GPCallback callback,
  void * param
)
{
	GPIConnection * iconnection;
	if((connection == NULL) || (*connection == NULL) || (profile == 0))
		return GP_PARAMETER_ERROR;
	if(callback == NULL)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e042c);
	iconnection = (GPIConnection *)*connection;
	if(iconnection->simulation)
	{
		GPGetInfoResponseArg arg={0};
		callback(connection, &arg, param);
		return GP_NO_ERROR;
	}
	if(iconnection->connectState == GPI_DISCONNECTED)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0440);
	return gpiGetInfo(connection, profile, checkCache, blocking, callback, param);
}
