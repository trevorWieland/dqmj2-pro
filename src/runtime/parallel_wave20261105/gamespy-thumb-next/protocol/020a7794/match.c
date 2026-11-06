#include "context.h"
int native_main_020a7794(SBServerList *slist, char *buf, int len)
{
	int numkeys;
	int i;
	int strindex;
	numkeys = native_fn_020a8640(slist->keylist);
	for (i = 0 ; i < numkeys ; i++)
	{
		switch (((KeyInfo *)native_fn_020a8644(slist->keylist, i))->keyType)
		{
		case KEYTYPE_BYTE:
			buf++;
			len--;
			break;
		case KEYTYPE_SHORT:
			buf += 2;
			len -= 2;
			break;
		case KEYTYPE_STRING:
			if (len < 1)
				return 0; 
			strindex = (unsigned char)(buf[0]);
			buf++;
			len--;
			if (strindex == 0xFF) 
			{
				strindex = native_fn_020a6fa8(buf, len);
				if (strindex == -1) 
					return 0;
				buf += strindex;
				len -= strindex;
			} 
			break;
		default:
			assert(0);
			return 0; 
		}
		if (len < 0)
			return 0; 
	}
	return 1;
}