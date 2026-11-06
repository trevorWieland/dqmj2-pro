#include "context.h"
void native_main_020a5710(GOACryptState *state, unsigned char *key, unsigned char keysize)
{
    
    
    
    
    
    
    
	
    int i;
    unsigned char toswap, swaptemp, rsum;
    unsigned keypos;
	
    
	
    if (keysize < 1)
	{
        GOAHashInit(state);
        return;
	}
	
    
	
    for (i=0;i<256;i++)
        state->cards[i] = (unsigned char)(i);
	
    
	
    toswap = 0;
    keypos = 0;         
    rsum = 0;
    for (i=255;i>=0;i--)
	{
        toswap = keyrand(state, i, key, keysize, &rsum, &keypos);
        swaptemp = state->cards[i];
        state->cards[i] = state->cards[toswap];
        state->cards[toswap] = swaptemp;
	}
	
    
    
    
    
	
    state->rotor = state->cards[1];
    state->ratchet = state->cards[3];
    state->avalanche = state->cards[5];
    state->last_plain = state->cards[7];
    state->last_cipher = state->cards[rsum];
	
    toswap = swaptemp = rsum = 0;
    keypos = 0;
}