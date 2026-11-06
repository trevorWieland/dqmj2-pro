#include "context.h"
unsigned char native_main_020a5660(GOACryptState *state, int limit,
							 unsigned char *user_key,
							 unsigned char keysize,
							 unsigned char *rsum,
							 unsigned *keypos)
{
    unsigned int u,             
        retry_limiter,      
        mask;               
	
    if (!limit) return 0;   
    retry_limiter = 0;
    mask = 1;               
    while (mask < (unsigned)limit)    
        mask = (mask << 1) + 1;
    do
	{
        *rsum = (unsigned char)(state->cards[*rsum] + user_key[(*keypos)++]);
        if (*keypos >= keysize)
		{
            *keypos = 0;            
            *rsum = (unsigned char)(*rsum + keysize);   
		}
        u = mask & *rsum;
        if (++retry_limiter > 11)
            u %= (unsigned int)limit;     
	}
    while (u > (unsigned)limit);
    return (unsigned char)(u);
}