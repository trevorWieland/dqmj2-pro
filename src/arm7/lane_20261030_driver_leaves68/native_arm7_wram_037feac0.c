#include "native_sound_register_types.h"
void native_arm7_wram_037feac0(s32 channel, s32 timer)
{
    NativeRegister(channel)->timer = (u16)(65536u - (u32)timer);
}
