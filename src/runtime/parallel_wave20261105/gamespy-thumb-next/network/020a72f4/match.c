#include "context.h"
void native_main_020a72f4(SBServerList *slist)
{
	int i;
	int oddmode;

	slist->mychallenge[0] = (char)(33 + native_fn_0201d5d4() % 93); 
	oddmode = 0;
	for (i = 1; i < LIST_CHALLENGE_LEN ; i++)
	{
		oddmode = CALCULATEODDMODE(slist->mychallenge,i, oddmode);
		slist->mychallenge[i] = (char)(33 + native_fn_0201d5d4() % 93); 
		
		if ((oddmode && (slist->mychallenge[i] & 1) == 0) || (!oddmode && ((slist->mychallenge[i] & 1) == 1)))
			slist->mychallenge[i]++;

	}
}