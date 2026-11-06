#include "context.h"
void native_main_020a932c(const char * gamename)
{
	char hostname[64];
	int override;
	int rcode;
	int len;

	GS_ASSERT(gamename)

	
	strcpy(__GSIACGamename, gamename);

	
	AC.sock = INVALID_SOCKET;

	
	SocketStartUp();

	
	override = GSIACHostname[0];
	if(!override)
		sprintf(hostname, native_data_020e03f4, gamename);

	
	rcode = get_sockaddrin(override?GSIACHostname:hostname, MASTER_PORT, &native_data_021d2474);
	if(!rcode)
		return;

	
	AC.sock = socket(AF_INET, SOCK_DGRAM, 0);
	if(AC.sock == INVALID_SOCKET)
		return;

	
	AC.packet[0] = PACKET_TYPE;
	len = (int)strlen(gamename);
	memcpy(native_data_021d2481, gamename, (size_t)len + 1);
	AC.packetLen = (len + 6);

	
	SendPacket();

	
	AC.retryCount = 0;
}