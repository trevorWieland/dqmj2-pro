typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

typedef struct {
    u8 *pointer;
    u32 length;
} NativeSpan;

extern u32 native_fn_0203cc2c(u8 *, u32);
extern void native_fn_0204518c(NativeSpan *, u32, u32);
extern void native_fn_020481b8(u8 *, u32, u32);
extern void native_fn_0202a498(u32, u32);
extern void native_fn_0204bbec(void);
extern void native_fn_02046150(u32, u32, u32);
extern void native_fn_020462e0(u32, u32, u32);
extern void native_fn_020848d0(void);
extern void native_fn_020489f0(u32);
extern void native_fn_ov001_021f1a08(void);
extern void native_fn_02045654(u32);
extern u8 *native_fn_020462cc(u32);
extern void native_fn_ov001_021f0f60(u8 *);
extern void native_fn_02048308(void);
extern u8 native_data_ov001_0222ecb4[];
extern u8 native_data_ov001_02238f58[];

void native_ov001_021f0f98(void) {
    NativeSpan span;
    u16 zero;
    u32 resource;

    zero = 0;
    resource = native_fn_0203cc2c(native_data_ov001_0222ecb4, 1);
    native_fn_0204518c(&span, resource, 0);
    native_fn_020481b8(span.pointer, 0, span.length);
    native_fn_0202a498(1, resource);
    native_fn_0204bbec();
    native_fn_02046150(0, 1, 2);
    native_fn_020462e0(0, 2, 1);
    native_fn_020848d0();
    native_fn_020489f0(0);
    native_fn_020481b8((u8 *)&zero, 0, 2);
    native_fn_ov001_021f1a08();
    *native_data_ov001_02238f58 = 3;
    native_fn_02045654(1);
    native_fn_02045654(2);
    native_fn_ov001_021f0f60(*(u8 **)(native_fn_020462cc(0) + 8) + 0x20);
    native_fn_02048308();
}
