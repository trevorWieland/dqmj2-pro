#include "native_card_callback_types.h"
void native_arm7_wram_03802974(CardTransfer *state)
{
    SPI_DATA=0;
    while(SPI_CONTROL&0x80) {}
    if((SPI_DATA&255)!=*state->source) {
        state->matched=0;
        if(state->count>1) state->count=1;
    }
    state->source++;
}
