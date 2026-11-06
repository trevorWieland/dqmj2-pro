#include "context.h"
SBError native_main_020a7fb0(SBServerList *slist, char *buf, int len)
{
	time_t changeTime;
	unsigned int ip;
	unsigned short port;
	SBServer server;
	unsigned char mapCount;
	int i;
	char *mapList[MAX_MAPLOOP_LENGTH];
	if (len < 11)
		return sbe_dataerror; 
	memcpy(&ip, buf, 4);
	memcpy(&port, buf + 4, 2);
	i = native_fn_020a6de4(slist, ip, port);
	if (i == -1)
		return sbe_noerror; 
	server = native_fn_020a6e9c(slist, i);
	memcpy(&changeTime, buf + 6, 4);
	changeTime = (time_t)ntohl((unsigned long)changeTime);
	mapCount = (unsigned char)buf[10];
	buf += 11;
	len -= 11;
	for (i = 0 ; i < mapCount && i < MAX_MAPLOOP_LENGTH; i++)
	{
		int maplen;
		if (len < 1)
			break;
		maplen = native_fn_020a6fa8(buf, len);
		if (maplen == -1)
			return sbe_dataerror; 
		mapList[i] = buf;
		buf += maplen;
		len -= maplen;
	}
	if (slist->MaploopCallback == NULL)
		return sbe_noerror;
	slist->MaploopCallback(slist, server, changeTime, i, mapList, slist->instance);
	return sbe_noerror;
}