#include "context.h"
int native_main_020a7858(SBServerList *slist, SBServer server, char *buf, int len, int usepopularlist)
{
	int numkeys;
	int i;
	short sval;
	int strindex;
	int holdlen = len;
	goa_uint32 ip;
	unsigned short port;
	unsigned char flags;


	flags = (unsigned char)buf[0];
	native_fn_020a6538(server, flags);
	buf++;
	len--;

	
	buf += 4;
	len -= 4;
		
	
	if (flags & NONSTANDARD_PORT_FLAG)
	{
		buf += 2;
		len -= 2;
	}

	if (flags & PRIVATE_IP_FLAG)
	{
		memcpy(&ip, buf, 4);
		buf += 4;
		len -= 4;
	} else
		ip = 0;
	if (flags & NONSTANDARD_PRIVATE_PORT_FLAG)
	{
		memcpy(&port, buf, 2);
		buf += 2;
		len -= 2;
	} else
		port = slist->defaultport;
	native_fn_020a653c(server, ip, port);
	if (flags & ICMP_IP_FLAG)
	{
		memcpy(&ip, buf, 4);
		buf += 4;
		len -= 4;
		native_fn_020a6544(server, ip);
	}
	
	if (flags & HAS_KEYS_FLAG) 
	{	
		numkeys = native_fn_020a8640(slist->keylist);
		for (i = 0 ; i < numkeys ; i++)
		{
			KeyInfo *ki = (KeyInfo *)native_fn_020a8644(slist->keylist, i);
			switch (ki->keyType)
			{
				case KEYTYPE_BYTE:
					native_fn_020a5fc0(server, ki->keyName, (unsigned char)buf[0]);
					buf++;
					len--;
					break;
				case KEYTYPE_SHORT:
					memcpy(&sval, buf, 2);
					native_fn_020a5fc0(server, ki->keyName, ntohs((unsigned short)sval));
					buf += 2;
					len -= 2;
					break;
				case KEYTYPE_STRING:
					if (usepopularlist)
					{
						strindex = (unsigned char)(buf[0]);
						buf++;
						len--;
					} else
						strindex = 0xFF;
					if (strindex == 0xFF) 
					{
						native_fn_020a5f98(server, ki->keyName, buf);
						strindex = (int)native_fn_0201d69c(buf) + 1;
						buf += strindex;
						len -= strindex;
					} else 
					{
						native_fn_020a5f98(server, ki->keyName, slist->popularvalues[strindex]);
					}
					break;
			}
		
		}
		native_fn_020a6548(server, (unsigned char)(native_fn_020a654c(server) | STATE_BASICKEYS));
	}
	if (flags & HAS_FULL_RULES_FLAG) 
	{
		while (*buf && len > 0)
		{
			char *k = buf;
			i = (int)native_fn_0201d69c(k) + 1;
			buf += i;
			len -= i;
			native_fn_020a5f98(server, k, buf);
			i = (int)native_fn_0201d69c(buf) + 1;
			buf += i;
			len -= i;
		}
		buf++;
		len--; 
		native_fn_020a6548(server, (unsigned char)(native_fn_020a654c(server) | STATE_FULLKEYS));
	}
	
	
	
	{
		unsigned char state = native_fn_020a654c(server);
		if ((flags & (HAS_FULL_RULES_FLAG|HAS_KEYS_FLAG)) == 0 && ((state & STATE_BASICKEYS) | (state & STATE_FULLKEYS)))
		{
			state &= (unsigned char)~(STATE_BASICKEYS|STATE_FULLKEYS);
			native_fn_020a6548(server, state);
		}
	}
	return holdlen - len;
}