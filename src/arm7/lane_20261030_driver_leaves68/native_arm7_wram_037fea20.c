#include "native_sound_register_types.h"
void native_arm7_wram_037fea20(s32 channel, s32 hold)
{
    volatile struct NativeSoundRegister *reg = NativeRegister(channel);
    u32 control = reg->control & ~0x80000000u;
    if (hold & 1)
        control |= 0x8000;
    reg->control = control;
}
