typedef unsigned char u8;
typedef unsigned int u32;
typedef int s32;
typedef struct {
    u8 unknown_00[0x1c];
    u32 handle;
} State;
extern State native_data_01fff960;
extern u8 native_data_021cebe0[];
extern void native_fn_0205fa4c(State *, s32);
extern u8 *native_fn_0205f98c(u32, u32);

void native_itcm_01ffb060(s32 value) {
    u8 *target;
    if (value == 1) {
        native_data_021cebe0[4] = 2;
    } else {
        native_data_021cebe0[4] = 0;
    }
    if (native_data_01fff960.handle == 0) {
        return;
    }
    native_fn_0205fa4c(&native_data_01fff960, value);
    target = native_fn_0205f98c(native_data_01fff960.handle, 0);
    *(u32 *)(target + 0x7c) &= ~2u;
}
