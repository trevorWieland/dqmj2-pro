#include "context.h"
unsigned char native_main_020a578c(GOACryptState *state, unsigned char b)
{
    unsigned char swaptemp;
	
    
	
    state->ratchet = (unsigned char)(state->ratchet + state->cards[state->rotor++]);
    swaptemp = state->cards[state->last_cipher];
    state->cards[state->last_cipher] = state->cards[state->ratchet];
    state->cards[state->ratchet] = state->cards[state->last_plain];
    state->cards[state->last_plain] = state->cards[state->rotor];
    state->cards[state->rotor] = swaptemp;
    state->avalanche = (unsigned char)(state->avalanche + state->cards[swaptemp]);
	
    
    
	
	
	state->last_plain = (unsigned char)(b^state->cards[(state->cards[state->avalanche] + state->cards[state->rotor]) & 0xFF] ^
		state->cards[state->cards[(state->cards[state->last_plain] +
		state->cards[state->last_cipher] +
		state->cards[state->ratchet])&0xFF]]);
    state->last_cipher = b;
    return state->last_plain;
}