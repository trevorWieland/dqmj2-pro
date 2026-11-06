#include "native_card_callback_types.h"
void native_arm7_wram_038028e4(CardTransfer *state)
{
    SPI_DATA=0;
    while(SPI_CONTROL&0x80) {}
    *state->destination=SPI_DATA;
    state->destination++;
}
