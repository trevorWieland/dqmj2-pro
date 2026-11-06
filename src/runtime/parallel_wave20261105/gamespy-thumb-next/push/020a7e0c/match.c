#include "context.h"
SBError native_main_020a7e0c(SBServerList *slist, char *buf, int len)
{
	int i;
	int numkeys;
	
	numkeys = (unsigned char)buf[0];
	buf++;
	len--;
	
	if (slist->keylist != NULL) 
	{
		native_fn_020a75ec(slist);
	}
	slist->keylist = native_fn_020a85dc(sizeof(KeyInfo), numkeys, NULL);
	if (slist->keylist == NULL)
		return sbe_allocerror;
	for (i = 0 ; i < numkeys ; i++)
	{
		int keylen;
		KeyInfo ki;
		if (len < 2)
			return sbe_dataerror; 
		keylen = native_fn_020a6fa8(buf + 1, len - 1);
		if (keylen == -1)
			return sbe_dataerror; 
		ki.keyType = (unsigned char)(buf[0]);
		ki.keyName = native_fn_020a6f34(slist, buf + 1);
		native_fn_020a865c(slist->keylist, &ki);
		buf += keylen + 1;
		len -= keylen + 1;
	}
	return sbe_noerror;	
}