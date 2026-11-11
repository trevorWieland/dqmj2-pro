typedef unsigned char u8;
typedef unsigned int u32;

extern void native_fn_02089804(void);
extern void native_fn_02006b7c(u32);
extern u32 native_fn_02084718(void);
extern void native_fn_02084180(u32);
extern void native_fn_020841b8(void);
extern void native_fn_020c2528(void);
extern u8 native_data_021d4c3c[];

void native_main_020c225c(void *handle) {
    u8 *state;
    if (native_data_021d4c3c[1] != 0) return;
    native_fn_02089804();
    native_fn_02006b7c(100);
    state = native_data_021d4c3c;
    *(u32 *)(state + 0x18) = (u32)handle;
    state[1] = 1;
    if (native_fn_02084718() == 1) {
        native_fn_02084180(1);
        native_fn_020841b8();
    }
    *(u32 *)(native_data_021d4c3c + 0x8) = 0;
    while (1) {
        native_fn_020c2528();
    }
}
