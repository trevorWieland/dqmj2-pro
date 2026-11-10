typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

extern u8 native_data_02101ae8[];
extern u8 native_data_ov003_021e041c[];
extern u8 native_data_ov003_021e0420[];
extern u8 native_data_ov003_021e0d18[];

extern u32 native_fn_0205f9e4(u32);
extern void native_fn_02049130(s32, s32, u32);
extern void native_fn_ov003_021e002c(void);
extern void native_fn_0206b35c(void);

#define FIELD(base, type, offset) (*(type *)((u8 *)(base) + (offset)))

/* Release the overlay's staged resources when the mode calls for it, then mark
   the rebuild latch for the caller. */
void native_ov003_021dff60(u8 *context) {
    s32 found = 0;

    if (native_data_ov003_021e041c[1] != 0) {
        if ((s8)context[0x10] == 7) {
            native_fn_ov003_021e002c();
            native_fn_0205f9e4(FIELD(native_data_ov003_021e0d18, u32, 0x10));
        } else {
            native_fn_02049130((s32)context, 8, FIELD(native_data_ov003_021e0d18, u32, 0x10));
            native_fn_0205f9e4(FIELD(native_data_ov003_021e0d18, u32, 0x10));
        }
    }
    {
        s8 i = 0;
        u8 *entry = native_data_ov003_021e0420;
        do {
            if (*entry != 0) {
                found = 1;
            }
            entry++;
            i++;
        } while (i < 2);
    }
    if (found != 0) {
        native_fn_0205f9e4(FIELD(native_data_ov003_021e0d18, u32, 0x14));
    }
    if ((s8)context[0x10] == 3) {
        native_fn_0206b35c();
    }
    FIELD(native_data_02101ae8, u32, 0xc84) = 1;
}


