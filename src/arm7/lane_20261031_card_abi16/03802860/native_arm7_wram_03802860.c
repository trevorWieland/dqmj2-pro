#include "native_card_service_types.h"
void native_arm7_wram_03802860(const void *source,void *destination,u32 length,void (*transfer)(CardTransfer *))
{
    CardTransfer *state=&CARD_TRANSFER;
    state->source=source;
    state->destination=destination;
    CARD_SPI_CONTROL=0xa040;
    while(length!=0) {
        if(--state->count==0) CARD_SPI_CONTROL=0xa000;
        while(CARD_SPI_CONTROL&0x80) {}
        transfer(state);
        --length;
    }
    if(state->count==0) CARD_SPI_CONTROL=0;
}
