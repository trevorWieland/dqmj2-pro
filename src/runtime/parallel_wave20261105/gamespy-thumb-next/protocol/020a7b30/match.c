#include "context.h"
SBError native_main_020a7b30(SBServerList *slist)
{
	int reqlen;
	int keyoffset;
	int keylen;
	char *inbuf = slist->inbuffer;
	int inlen = slist->inbufferlen;
	switch (slist->pstate)
	{
	case pi_cryptheader:
		if (inlen < 1)
			break;
		reqlen = (((unsigned char)(inbuf[0])) ^ 0xEC) + 2;
		if (inlen < reqlen)
			break; 
		keyoffset = reqlen;
		keylen = ((unsigned char)(inbuf[reqlen - 1])) ^ 0xEA;
		reqlen += keylen;
		if (inlen < reqlen)
			break; 
		
		native_fn_020a76a0(slist, inbuf + keyoffset, keylen);
		slist->pstate = pi_fixedheader;

		
		
		memcpy(&slist->backendgameflags, &inbuf[1], 2);
		slist->backendgameflags = ntohs(slist->backendgameflags);

		inbuf += reqlen;
		inlen -= reqlen;
		
		native_fn_020a5820(&(slist->cryptkey), (unsigned char *)inbuf, inlen);
		
	case pi_fixedheader:
		if (inlen < FIXED_HEADER_LEN)
			break;
		memcpy(&slist->mypublicip, inbuf, 4);
		slist->ListCallback(slist, slc_publicipdetermined, SBNullServer, slist->instance);
		memcpy(&slist->defaultport, inbuf + 4, 2);
		if (slist->defaultport == 0xFFFF) 
		{
			if (native_fn_020a6fa8(inbuf + FIXED_HEADER_LEN, inlen - FIXED_HEADER_LEN) == -1) 
				break;
			native_fn_020a7b28(slist, inbuf + FIXED_HEADER_LEN);
			
			slist->ListCallback(slist, slc_queryerror, SBNullServer, slist->instance);
			if (slist->inbuffer == NULL)
				break;
		}
		inbuf += FIXED_HEADER_LEN;
		inlen -= FIXED_HEADER_LEN;
		if ((slist->queryoptions & NO_SERVER_LIST) || slist->defaultport == 0xFFFF)
		{
			slist->pstate = pi_finished;
			slist->state = sl_connected;
			break; 
		}
		slist->pstate = pi_keylist;
		slist->expectedelements = -1;
		
		
	case pi_keylist:
		if (slist->expectedelements == -1) 
		{
			if (inlen < 1)
				break;
			slist->expectedelements = (unsigned char)(inbuf[0]);
			slist->keylist = native_fn_020a85dc(sizeof(KeyInfo), slist->expectedelements, NULL);
			if (slist->keylist == NULL) 
				return sbe_allocerror;
			inbuf++;
			inlen--;
		}
		
		while (slist->expectedelements > native_fn_020a8640(slist->keylist))
		{
			KeyInfo ki;
			int keylen;
			if (inlen < 2)
				break; 
			keylen = native_fn_020a6fa8(inbuf + 1, inlen - 1);
			if (keylen == -1)
				break; 
			ki.keyType = (unsigned char)(inbuf[0]);
			ki.keyName = native_fn_020a6f34(slist, inbuf + 1);
			native_fn_020a865c(slist->keylist, &ki);
			inbuf += keylen + 1;
			inlen -= keylen + 1;
		}
		if (slist->expectedelements > native_fn_020a8640(slist->keylist))
			break; 
		
		slist->pstate = pi_uniquevaluelist;
		slist->expectedelements = -1;
	case pi_uniquevaluelist:
		if (slist->expectedelements == -1) 
		{
			if (inlen < 1)
				break;
			slist->expectedelements = (unsigned char)(inbuf[0]);
			slist->numpopularvalues = 0;
			inbuf++;
			inlen--;
		}
		while (slist->expectedelements > slist->numpopularvalues)
		{
			int keylen = native_fn_020a6fa8(inbuf, inlen);
			if (keylen == -1)
				break; 
			slist->popularvalues[slist->numpopularvalues++] = native_fn_020a6f34(slist, inbuf);
			inbuf += keylen;
			inlen -= keylen;
		}
		if (slist->expectedelements > slist->numpopularvalues)
			break; 
		
		slist->pstate = pi_servers;		
	case pi_servers :
		if (inlen < 5) 
			break;
		do
		{
			reqlen =  native_fn_020a7a5c(slist, inbuf, inlen);
			if (reqlen == -2)
				return sbe_allocerror;			
			else if (reqlen == -1) 
			{
				inlen -= 5;
				inbuf += 5;
				slist->pstate = pi_finished;
				slist->state = sl_connected;
				slist->ListCallback(slist, slc_initiallistcomplete, SBNullServer, slist->instance);
				break;
			}
			inbuf += reqlen;
			inlen -= reqlen;
			if (slist->inbuffer == NULL)
				reqlen = 0; 
		} while (reqlen != 0);
		break;
	default:
		break;
	}
	assert(inlen >= 0);
	if (slist->inbuffer == NULL)
		return sbe_noerror; 
	if (inlen != 0) 
	{
		native_fn_0201b1bc(slist->inbuffer, inbuf, (size_t)inlen);
	}
	slist->inbufferlen = inlen;
	

	return sbe_noerror;
}