#include "context.h"
GPResult native_main_020aa7c0(
  GPConnection * connection,
  GPProfile profile,
  const char * message
)
{
	GPIConnection * iconnection;
	if((connection == NULL) || (*connection == NULL))
		return GP_PARAMETER_ERROR;
	iconnection = (GPIConnection *)*connection;
	if(iconnection->simulation)
		return GP_NO_ERROR;
	if(iconnection->connectState == GPI_DISCONNECTED)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0440);
	if(message == NULL)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0534);
	return gpiSendBuddyMessage(connection, profile, GPI_BM_MESSAGE, message, 0, NULL);
}
