#include "context.h"
GPResult
native_main_020b2b24(
  GPConnection * connection,
  SOCKET sock,
  int * state
)
{
	int aWriteFlag  = 0;
	int aExceptFlag = 0;
	int aReturnCode = 0;
	aReturnCode = GSISocketSelect(sock, NULL, &aWriteFlag, &aExceptFlag);
	if ( gsiSocketIsError(aReturnCode))
	{
		gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_HotError,
			"Error connecting\n");
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e15a8);
	}
	if (aReturnCode > 0)
	{
		if(aExceptFlag)
		{
			gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_HotError,
				"Connection rejected\n");
			*state = GPI_DISCONNECTED;
			return GP_NO_ERROR;
		}
		if(aWriteFlag)
		{
			gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_Notice,
				"Connection accepted\n");
			*state = GPI_CONNECTED;
			return GP_NO_ERROR;
		}
	}
	*state = GPI_NOT_CONNECTED;
	return GP_NO_ERROR;
}
