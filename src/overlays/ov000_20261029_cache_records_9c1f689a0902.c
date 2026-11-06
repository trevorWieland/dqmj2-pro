typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Lease;
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_020485b4(Lease *);
extern void func_020484dc(u32, u32);
extern void func_02048308(void);

typedef struct { u8 reserved; u8 handle; u8 padding[2]; Lease *lease; u32 reserved2[2]; void *record; } State_0221d6f8;
extern State_0221d6f8 data_ov000_02246318;
extern const char data_ov000_0222fb4c[];
u32 native_ov000_0221d6f8(void) {
    u8 handle = func_02048404(1, data_ov000_0222fb4c, 4, 2);
    data_ov000_02246318.handle = handle;
    if (handle != 255) {
        data_ov000_02246318.lease = func_0204854c(1, handle);
        if (data_ov000_02246318.lease) {
            data_ov000_02246318.record = data_ov000_02246318.lease->record;
            if (data_ov000_02246318.record) {
                func_02048308();
                return 1;
            }
            func_020485b4(data_ov000_02246318.lease);
        }
        func_020484dc(1, data_ov000_02246318.handle);
    }
    return 0;
}

typedef struct { u8 handle; u8 padding[15]; Lease *lease; void *record; } State_02221aa4;
extern State_02221aa4 data_ov000_02246438;
extern const char data_ov000_0222fbbc[];
u32 native_ov000_02221aa4(void) {
    u8 handle = func_02048404(1, data_ov000_0222fbbc, 4, 2);
    data_ov000_02246438.handle = handle;
    if (handle != 255) {
        data_ov000_02246438.lease = func_0204854c(1, handle);
        if (data_ov000_02246438.lease) {
            data_ov000_02246438.record = data_ov000_02246438.lease->record;
            if (data_ov000_02246438.record) {
                
                return 1;
            }
            func_020485b4(data_ov000_02246438.lease);
        }
        func_020484dc(1, data_ov000_02246438.handle);
    }
    return 0;
}
