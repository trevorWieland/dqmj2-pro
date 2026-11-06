#include "context.h"
GSIACResult native_main_020a9448(void)
{
	char packet[64];
	SOCKADDR_IN address;
	int len = sizeof(address);
	int rcode;
	int disabledservices;

	
	if(AC.sock == INVALID_SOCKET)
	{
		__GSIACResult = GSIACAvailable;
		return __GSIACResult;
	}

	
	if(CanReceiveOnSocket(AC.sock))
	{
		
		rcode = (int)recvfrom(AC.sock, packet, (int)sizeof(packet), 0, (SOCKADDR *)&address, &len);

		
		rcode = HandlePacket(packet, rcode, &address, &disabledservices);
		if(rcode == 0)
		{
			
			closesocket(AC.sock);

			
			if(disabledservices & 1)
				__GSIACResult = GSIACUnavailable;
			else if(disabledservices & 2)
				__GSIACResult = GSIACTemporarilyUnavailable;
			else
				__GSIACResult = GSIACAvailable;

			
			return __GSIACResult;
		}
	}

	
	if(current_time() > (AC.sendTime + TIMEOUT_TIME))
	{
		
		if(AC.retryCount == MAX_RETRIES)
		{
			
			closesocket(AC.sock);
			__GSIACResult = GSIACAvailable;
			return __GSIACResult;
		}

		
		SendPacket();
		AC.retryCount++;
	}

	return GSIACWaiting;
}