#include "context.h"
SBError native_main_020a7e94(SBServerList *slist, char *buf, int len)
{
	unsigned char isFinal;
	unsigned char resultCount;
	unsigned int ip;
	unsigned short port;
	char *nick;
	time_t lastSeen;
	int i;

	if (len < 2)
		return sbe_dataerror; 
	isFinal = (unsigned char)buf[0];
	resultCount = (unsigned char)buf[1];
	buf += 2;
	len -= 2;
	for (i = 0 ; i < resultCount ; i++)
	{
		int slen;
		nick = buf;
		slen = native_fn_020a6fa8(buf, len);
		if (slen == -1)
			return sbe_dataerror;
		buf += slen;
		len -= slen;
		if (len < 11)
			return sbe_dataerror; 
		memcpy(&ip, buf, 4);
		memcpy(&port, buf + 4, 2);
		memcpy(&lastSeen, buf + 6, 4);
		lastSeen  = (time_t)ntohl((unsigned long)lastSeen);
		buf += 10;
		len -= 10;
		slen = native_fn_020a6fa8(buf, len);
		if (slen == -1)
			return sbe_dataerror; 
		slist->PlayerSearchCallback(slist, nick, ip, port, lastSeen, buf, slist->instance);
		
		buf += slen;
		len -= slen;
	}
	if (isFinal) 
		slist->PlayerSearchCallback(slist, NULL, 0, 0, 0, NULL, slist->instance);


	return sbe_noerror;

}