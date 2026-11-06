typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct NativeSelectorContext {
    u8 opaque00[0x1c];
    u32 value1c;
    u8 opaque20[0xb8];
    u32 valued8;
    u8 opaquedc[10];
    u16 modee6;
} NativeSelectorContext;
typedef struct NativeSelectorGlobal {
    u8 opaque[0x550];
    NativeSelectorContext *current;
} NativeSelectorGlobal;
extern NativeSelectorGlobal native_host_arm7_data_027f8884;
extern u32 native_host_arm7_data_0380b4bc[];
extern u32 native_host_arm7_arm_037fda38(void *);
extern u32 native_host_arm7_arm_037fd898(void *, s16, s16, s32, s32);
extern void native_host_arm7_arm_027e5f98();
extern void native_host_arm7_arm_027e5c5c();
u32 native_arm7_main_027e5bac(void)
{
    u32 *alarm = native_host_arm7_data_0380b4bc;
    NativeSelectorContext *context = native_host_arm7_data_027f8884.current;
    u16 mode = context->modee6;
    if (mode == 1)
    {
        if (*native_host_arm7_data_0380b4bc != 0)
            native_host_arm7_arm_037fda38(native_host_arm7_data_0380b4bc);
        return native_host_arm7_arm_037fd898(native_host_arm7_data_0380b4bc, 203, 263, (s32)native_host_arm7_arm_027e5f98, 3);
    }
    else if (mode == 2)
    {
        context->value1c = 0;
        if (*native_host_arm7_data_0380b4bc != 0)
            native_host_arm7_arm_037fda38(native_host_arm7_data_0380b4bc);
        native_host_arm7_arm_037fd898(native_host_arm7_data_0380b4bc, 200, 263, (s32)native_host_arm7_arm_027e5c5c, 1);
        alarm = 0;
        context->valued8 = 0;
    }
    return (u32)alarm;
}
