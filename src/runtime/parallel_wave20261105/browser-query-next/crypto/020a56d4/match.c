#include "context.h"
void native_main_020a56d4(GOACryptState *state)
{
    
    
	
    int i, j;
	
    
	
    state->rotor = 1;
    state->ratchet = 3;
    state->avalanche = 5;
    state->last_plain = 7;
    state->last_cipher = 11;
	
    
	
    for (i=0, j=255;i<256;i++,j--)
        state->cards[i] = (unsigned char) j;
}