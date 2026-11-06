#include "context.h"
GPResult
native_main_020afb68(
  GPConnection * connection,
  GPIOperation * operation,
  const char * input
)
{
	GPResult result = GP_NO_ERROR;

	
	
	switch(operation->type)
	{
	case GPI_CONNECT:
		result = gpiProcessConnect(connection, operation, input);
		break;

	case GPI_NEW_PROFILE:
		result = gpiProcessNewProfile(connection, operation, input);
		break;
	
	case GPI_DELETE_PROFILE:
		result = gpiProcessDeleteProfle(connection, operation, input);
		break;

	case GPI_GET_INFO:
		result = gpiProcessGetInfo(connection, operation, input);
		break;

	case GPI_REGISTER_UNIQUENICK:
		result = gpiProcessRegisterUniqueNick(connection, operation, input);
		break;

	case GPI_REGISTER_CDKEY:
		result = gpiProcessRegisterCdKey(connection, operation, input);
		break;

	default:
		gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Misc, GSIDebugLevel_HotError,
			"gpiProcessOperation was passed an operation with an invalid type (%d)\n", operation->type);
		assert(0);
		break;
	}

	if(result != GP_NO_ERROR)
		operation->result = result;
	
	return result;
}
