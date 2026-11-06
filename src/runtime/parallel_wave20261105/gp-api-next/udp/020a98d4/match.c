#include "context.h"
GT2Bool native_main_020a98d4(GT2Socket theSocket, unsigned int theIp, unsigned short thePort, GT2Byte * theMessage, 
							   int theMsgLen)
{
	GSUdpEngineObject *aUdp = gsUdpEngineGetEngine();
	char anAddr[GS_IP_ADDR_AND_PORT];
	if (aUdp->mAppUnknownMessage)
	{
		gsi_bool aRet;
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Comment, 
			"[Udp Engine] Unknown message from %s, passing to app\n", gt2AddressToString(theIp, thePort, anAddr));
		aRet = aUdp->mAppUnknownMessage(theIp, thePort, (unsigned char *)theMessage, (unsigned int)theMsgLen, aUdp->mAppUserData);
		return aRet ? GT2True : GT2False;
	}
	
	GSI_UNUSED(theSocket);
	GSI_UNUSED(anAddr);
	return GT2False;
}
