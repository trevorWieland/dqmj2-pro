typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Lease;
typedef struct {
    u8 handle;
    u8 flag;
    u8 padding[2];
    void *record;
    Lease *lease;
    void *buffer;
} State;
extern State data_ov001_0223df2c;
extern const char data_ov001_0222f0c4[];
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_020485b4(Lease *);
extern void func_020484dc(u32, u32);
extern void *func_0202a474(u32, u32);
extern void func_0204b1a0(void *);
extern void func_0204b4f4(void *, void *, u32, u32, u32, u32);
extern void func_0204b61c(void *, u32);
extern void func_02048308(void);

u32 native_ov001_0220a5e0(void) {
    u32 position;
    u8 handle;
    data_ov001_0223df2c.flag = 0;
    handle = func_02048404(1, data_ov001_0222f0c4, 4, 2);
    data_ov001_0223df2c.handle = handle;
    if (handle != 255) {
        data_ov001_0223df2c.lease = func_0204854c(1, handle);
        if (data_ov001_0223df2c.lease) {
            data_ov001_0223df2c.record = data_ov001_0223df2c.lease->record;
            if (data_ov001_0223df2c.record) {
                data_ov001_0223df2c.buffer = func_0202a474(72, 4);
                func_0204b1a0(data_ov001_0223df2c.record);
                func_0204b4f4(data_ov001_0223df2c.buffer, &position, 32, 2, 2, 36);
                func_0204b61c(data_ov001_0223df2c.buffer, 0);
                func_02048308();
                return 1;
            }
            func_020485b4(data_ov001_0223df2c.lease);
        }
        func_020484dc(1, data_ov001_0223df2c.handle);
    }
    return 0;
}
