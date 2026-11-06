#include "context.h"
int native_main_020a93cc(char * packet, int len, SOCKADDR_IN * address, int * disabledservices)
{
	int bitfield;

	
	if(len < 7)
		return 1;

	
	if(memcmp(&address->sin_addr, &native_data_021d2478, sizeof(IN_ADDR)) != 0)
		return 1;

	
	if(address->sin_port != AC.address.sin_port)
		return 1;

	
	if(memcmp(packet, native_data_020e0418, 3) != 0)
		return 1;

	
	
	bitfield = (int)((packet[3] << 24) & 0xFF000000);
	bitfield |= ((packet[4] << 16) & 0x00FF0000);
	bitfield |= ((packet[5] << 8) & 0x0000FF00);
	bitfield |= (packet[6] & 0x000000FF);

	
	*disabledservices = bitfield;

	return 0;
}