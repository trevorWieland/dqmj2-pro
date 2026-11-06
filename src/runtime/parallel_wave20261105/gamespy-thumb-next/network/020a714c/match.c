#include "context.h"
SBError native_main_020a714c(SBServerList *slist)
{
	struct   sockaddr_in saddr;
	struct hostent *hent;
	char masterHostname[128];
	int masterIndex;
	

	masterIndex = native_fn_020a710c(slist->queryforgamename, NUM_MASTER_SERVERS);
	if (SBOverrideMasterServer != NULL)
		native_fn_0201d6b8(masterHostname, SBOverrideMasterServer);
	else 
		native_fn_0200616c(masterHostname,native_data_020e0354, slist->queryforgamename, masterIndex);
	saddr.sin_family = AF_INET;
	saddr.sin_port = htons(MSPORT2);
	saddr.sin_addr.s_addr = native_fn_020a8c84(masterHostname);
	if (saddr.sin_addr.s_addr == INADDR_NONE)
	{
		hent = native_fn_0209046c(masterHostname);
		if (!hent)
			return sbe_dnserror; 
		memcpy(&saddr.sin_addr.s_addr,hent->h_addr_list[0], sizeof(saddr.sin_addr.s_addr));
	}

	if (slist->slsocket == INVALID_SOCKET)
	{
		slist->slsocket = native_fn_020a8b5c ( AF_INET, SOCK_STREAM, IPPROTO_TCP );
		if (slist->slsocket == INVALID_SOCKET)
			return sbe_socketerror;
	}
	if (native_fn_020a8bc4 ( slist->slsocket, (struct sockaddr *) &saddr, sizeof saddr ) != 0)
	{
		native_fn_020a8b6c(slist->slsocket);
		slist->slsocket = INVALID_SOCKET;
		return sbe_connecterror; 
	}
	
	
	return sbe_noerror;

}