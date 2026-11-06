#include "context.h"
GPResult
native_main_020b0cd4(
  GPConnection * connection,
  GPIOperation * operation
)
{
	GPISearchData * data = (GPISearchData*)operation->data;
	int rcode;
	struct sockaddr_in address;
	struct hostent * host;

	
	
	data->inputBuffer.size = 4096;
	data->inputBuffer.buffer = (char *)gsimalloc((unsigned int)data->inputBuffer.size + 1);
	if(data->inputBuffer.buffer == NULL)
		Error(connection, GP_MEMORY_ERROR, native_data_020e1170);

	
	
	data->sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if(data->sock == INVALID_SOCKET)
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e1180);

	
	
	rcode = SetSockBlocking(data->sock,0);
	if(rcode == 0)
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e11a8);

	
	
	
	
	
	
	host = gethostbyname(native_data_020e1130);
	if(host == NULL)
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e11dc);

	
	
	memset(&address, 0, sizeof(address));
	address.sin_family = AF_INET;
	address.sin_addr.s_addr = *(unsigned int *)host->h_addr_list[0];
	assert(address.sin_addr.s_addr != 0);
	address.sin_port = htons(GPI_SEARCH_MANAGER_PORT);
	rcode = connect(data->sock, (struct sockaddr *)&address, sizeof(struct sockaddr_in));
	if (gsiSocketIsError(rcode))
	{
		int error = GOAGetLastError(data->sock);
		if((error != WSAEWOULDBLOCK) && (error != WSAEINPROGRESS) && (error != WSAETIMEDOUT) )
		{
			CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e120c);
		}
	}

	
	
	operation->state = GPI_CONNECTING;
	data->searchStartTime = current_time();
	return GP_NO_ERROR;
}
