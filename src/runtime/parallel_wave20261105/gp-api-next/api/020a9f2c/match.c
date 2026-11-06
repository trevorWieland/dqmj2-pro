#include "context.h"
GPResult native_main_020a9f2c(
  GPConnection * connection,
  int productID,
  int namespaceID,
  int partnerID
)
{
	
	
	if(__GSIACResult != GSIACAvailable)
		return GP_PARAMETER_ERROR;

	
	
	if(connection == NULL)
		return GP_PARAMETER_ERROR;

	return gpiInitialize(connection, productID, namespaceID, partnerID);
}
