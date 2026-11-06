typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Lease;
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_02048308(void);
extern void func_0204b1a0(void *);
typedef struct { u8 handle; u8 padding[11]; Lease *lease; } State;
extern State data_ov000_02236da4;
extern const char data_ov000_0222eeac[];
extern u32 func_ov000_021f27fc(void);
extern void func_020485b4(Lease *);
extern void func_020484dc(u32, u32);
u32 native_ov000_021f28c0(void) {
    u8 handle = func_02048404(1, data_ov000_0222eeac, 4, 2);
    data_ov000_02236da4.handle = handle;
    if (handle != 255) {
        data_ov000_02236da4.lease = func_0204854c(1, handle);
        if (data_ov000_02236da4.lease) {
            if (func_ov000_021f27fc()) {
                return 1;
            }
            func_020485b4(data_ov000_02236da4.lease);
        }
        func_020484dc(1, data_ov000_02236da4.handle);
    }
    return 0;
}
