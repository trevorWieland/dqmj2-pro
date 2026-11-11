typedef unsigned char u8;
typedef unsigned int u32;

extern void native_fn_02026b28(void);
extern void native_fn_02026ec0(void);
extern void native_fn_020ba490(void);
extern void native_fn_0202718c(void);
extern u32 native_fn_020271ec(void);
extern void native_fn_02026f70(void);
extern void native_fn_0205f4f4(void);
extern void native_fn_020270d4(void);
extern void native_fn_020c225c(void);
extern void native_fn_020270d8(void);
extern u8 native_data_020ec9b8[];

void main(void) {
    u8 *state;
    native_fn_02026b28();
    native_fn_02026ec0();
    state = native_data_020ec9b8;
    while (1) {
        native_fn_020ba490();
        native_fn_0202718c();
        if (native_fn_020271ec() != 0) return;
        native_fn_02026f70();
        native_fn_0205f4f4();
        native_fn_020270d4();
        if (*(u32 *)(state + 0x10) != 0) native_fn_020c225c();
        native_fn_020270d8();
    }
}
