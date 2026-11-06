#include "context.h"
GPResult native_main_020aa2f8(
  GPConnection * connection,
  GPProfile profile
)
{
	GPIConnection * iconnection;

	
	
	if((connection == NULL) || (*connection == NULL))
		return GP_PARAMETER_ERROR;

	
	
	iconnection = (GPIConnection*)*connection;
	if(iconnection->simulation)
		return GP_NO_ERROR;

	
	
	if(iconnection->connectState == GPI_DISCONNECTED)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0440);

	return gpiAuthBuddyRequest(connection, profile);
}
