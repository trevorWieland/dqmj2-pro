typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
typedef volatile u32 vu32;
static inline vu32 OS_GetVBlankCount (void)
{
	return *(vu32 *)(0x02000000 + 0x007ffc3c) ;
}
void native_fn_020081fc(u8 * macAddress);
u16 native_main_02012340(void);
extern const u16 (*ctrdgi_fl_maxtime);
u16 native_main_02012340 (void)
{
    u8 mac[6];
    u16 ret;
    s32 i;
    native_fn_020081fc(mac);
    for (i = 0, ret = 0; i < 6; i++) {
        ret += mac[i];
    }
    ret += OS_GetVBlankCount();
    ret *= 7;
    return (u16)(200 + (ret % 20));
}
