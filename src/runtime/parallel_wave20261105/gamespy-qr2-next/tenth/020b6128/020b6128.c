#include "context.h"
void native_main_020b6128(const AddressMapping * theMap)
{
	if(theMap == NULL)
	{
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Comment,
			"ERROR: Port mapping not available.");
	}
	else
	{
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Comment,
			"Discovered map: [%s] -> [%s]\n", AddressToString(theMap->privateIp, theMap->privatePort, NULL),
											  AddressToString(theMap->publicIp,  theMap->publicPort,  NULL));
	}
}
