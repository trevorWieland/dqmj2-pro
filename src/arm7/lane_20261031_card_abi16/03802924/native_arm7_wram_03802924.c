#include "native_card_callback_types.h"
void native_arm7_wram_03802924(CardTransfer *state)
{
    volatile u16 readback;
    SPI_DATA=*state->source;
    state->source++;
    while(SPI_CONTROL&0x80) {}
    readback=SPI_DATA;
}
