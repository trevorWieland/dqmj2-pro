#include "native_channel_parameter_types.h"
void native_arm7_wram_037ffdb4(struct SNDLfo *lfo)
{
    if (lfo->delayCounter < lfo->param.delay)
    {
        lfo->delayCounter++;
        return;
    }
    else
    {
        u32 integral;
        integral = lfo->phase;
        integral += lfo->param.speed << 6;
        integral >>= 8;
        while (integral >= 128)
            integral -= 128;
        lfo->phase += lfo->param.speed << 6;
        lfo->phase &= 255;
        lfo->phase |= integral << 8;
    }
}
