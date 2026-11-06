#include "context.h"
GPResult native_main_020aa194(
  GPConnection * connection, 
  GPEnum info, 
  int value
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

	return gpiSetInfoi(connection, info, value);
}
