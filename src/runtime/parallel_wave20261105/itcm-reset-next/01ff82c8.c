#include "context.h"
void native_itcm_01ff82c8(void)
{
    u32 p=0x027ffe00;
    const u32 rom_base=*(u32 *)0x027ffc2c;
    if(rom_base>=0x8000)
        native_fn_01ff8370(rom_base,(void *)p,0x160);
    {
        u32 src_arm9=*(u32 *)(p+0x20);
        u32 dst_arm9=*(u32 *)(p+0x28);
        u32 len_arm9=*(u32 *)(p+0x2c);
        u32 src_arm7=*(u32 *)(p+0x30);
        u32 dst_arm7=*(u32 *)(p+0x38);
        u32 len_arm7=*(u32 *)(p+0x3c);
        {
            OSIntrMode bak_cpsr=native_fn_02007ff4();
            native_fn_02007270();
            native_fn_02007264();
            (void)native_fn_02008008(bak_cpsr);
        }
        native_fn_02007338();
        native_fn_0200732c();
        src_arm9+=rom_base;
        src_arm7+=rom_base;
        if(src_arm9<0x8000){
            u32 diff=0x8000-src_arm9;
            src_arm9=0x8000;
            dst_arm9+=diff;
            len_arm9-=diff;
        }
        native_fn_01ff8370(src_arm9,(void *)dst_arm9,(s32)len_arm9);
        native_fn_01ff8370(src_arm7,(void *)dst_arm7,(s32)len_arm7);
    }
}
