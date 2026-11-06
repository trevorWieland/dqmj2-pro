typedef unsigned char u8;
typedef unsigned int u32;
typedef signed short s16;
typedef struct { u32 flags; void *record; } Lease;
typedef struct { s16 x; s16 y; } Position;
typedef struct { u8 reserved[28]; void *field1c; } Buffer;
typedef struct { u8 reserved[0xC84]; u32 flag; } MainState;
extern MainState data_02101ae8;
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_020485b4(Lease *);
extern void func_020484dc(u32, u32);
extern void func_02048308(void);
extern void *func_0202a44c(u32, u32, u32);
extern void func_0204b1a0(void *);
extern void func_0204b4f4(void *, const void *, u32, u32, u32, u32);
extern void func_0204b61c(void *, u32);
extern void func_0204b85c(void *, const void *, u32, u32, u32, u32, u32);
extern void *func_0205f98c(void *, u32);
extern void func_02048a60(void *, u32, u32);
extern void func_0205fa4c(void *, u32);
typedef struct { u8 reserved[0xF2]; u8 handle; u8 padding[0x11]; Lease *lease; void *record; Buffer *buffer; Buffer *second; } State;
extern State data_ov000_022383e8;
extern const char data_ov000_0222f740[];
u32 native_ov000_02208638(void) {
    Position storage = {0, 0};
    data_ov000_022383e8.handle = func_02048404(1, data_ov000_0222f740, 4, 2);
    if (data_ov000_022383e8.handle != 255) {
        data_ov000_022383e8.lease = func_0204854c(1, data_ov000_022383e8.handle);
        if (data_ov000_022383e8.lease) {
            data_ov000_022383e8.record = data_ov000_022383e8.lease->record;
            if (data_ov000_022383e8.record) {
                data_02101ae8.flag = 1;
                func_02048308();
                data_ov000_022383e8.buffer = func_0202a44c(2, 72, 4);
                func_0204b1a0(data_ov000_022383e8.record);
                func_0204b4f4(data_ov000_022383e8.buffer, &storage, 32, 2, 2, 36);
                func_0204b61c(data_ov000_022383e8.buffer, 0);
                data_ov000_022383e8.second = func_0202a44c(2, 72, 4);
                func_0204b85c(data_ov000_022383e8.second, &storage, 8, 1, 0, 51, 0);
                func_02048a60(func_0205f98c(data_ov000_022383e8.second->field1c, 0), 224, 96);
                func_0205fa4c(data_ov000_022383e8.second, 0);
                return 1;
            }
            func_020485b4(data_ov000_022383e8.lease);
        }
        func_020484dc(1, data_ov000_022383e8.handle);
    }
    return 0;
}
