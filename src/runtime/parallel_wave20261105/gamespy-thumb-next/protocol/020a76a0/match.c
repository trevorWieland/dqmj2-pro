#include "context.h"
void native_main_020a76a0(SBServerList *slist, char *key, int keylen)
{
	
	int i;
	int seckeylen = (int)native_fn_0201d69c(slist->queryfromkey);
	char *seckey = slist->queryfromkey;
	for (i = 0 ; i < keylen ; i++)
	{
		slist->mychallenge[(i *  seckey[i % seckeylen]) % LIST_CHALLENGE_LEN] ^= (char)((slist->mychallenge[i % LIST_CHALLENGE_LEN] ^ key[i]) & 0xFF);
	}
	native_fn_020a5710(&(slist->cryptkey), (unsigned char *)(slist->mychallenge), LIST_CHALLENGE_LEN);

}