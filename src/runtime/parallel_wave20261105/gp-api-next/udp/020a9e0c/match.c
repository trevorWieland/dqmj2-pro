#include "context.h"
GSUdpErrorCode native_main_020a9e0c(char theHeader[GS_UDP_MSG_HEADER_LEN])
{
	GSUdpEngineObject *aUdp = gsUdpEngineGetEngine();
	GSUdpMsgHandler aHandler;
	int index;
	
	GS_ASSERT(aUdp->mInitialized);
	GS_ASSERT(theHeader);
	if (!aUdp->mInitialized)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
			"[Udp Engine] Engine not initialized\n");
		return GS_UDP_NETWORK_ERROR;
	}

	if (!theHeader || !theHeader[0])
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
			"[Udp Engine] invalid or empty header\n");
		return GS_UDP_PARAMETER_ERROR;
	}
	
	copy16(aHandler.mHeader, theHeader, GS_UDP_MSG_HEADER_LEN);

	index = ArraySearch(aUdp->mMsgHandlers, &aHandler, gsUdpMsgHandlerCompare2, 0, 0);
	if (index != NOT_FOUND)
	{
		ArrayDeleteAt(aUdp->mMsgHandlers, index);
	}
	return GS_UDP_NO_ERROR;
}
