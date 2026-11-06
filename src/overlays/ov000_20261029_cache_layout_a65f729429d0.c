typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Lease;
typedef struct { u8 handle; u8 padding[3]; void *record; Lease *lease; } State;
typedef struct { u8 padding[0xC84]; u32 flag; } MainState;
extern State data_ov000_022476f0;
extern MainState data_02101ae8;
extern u8 data_ov000_022476fc[];
extern u8 data_ov000_02247700[];
extern const char data_ov000_022300a0[];
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_020485b4(Lease *);
extern void func_020484dc(u32, u32);
extern void func_0204b1a0(void *);
extern void func_020c1de0(u32, void *, u32, u32, u32, u32);
extern void func_020c1c20(void *);
extern void func_020c1cf4(u32, void *, u32, int);
extern void func_02048308(void);

u32 native_ov000_0222aec4(void) {
    u8 handle = func_02048404(1, data_ov000_022300a0, 4, 2);
    data_ov000_022476f0.handle = handle;
    if (handle != 255) {
        data_ov000_022476f0.lease = func_0204854c(1, handle);
        if (data_ov000_022476f0.lease) {
            data_ov000_022476f0.record = data_ov000_022476f0.lease->record;
            if (data_ov000_022476f0.record) {
                func_0204b1a0(data_ov000_022476f0.record);
                func_020c1de0(2, data_ov000_02247700, 2, 36, 0, 32);
                data_02101ae8.flag = 1;
                func_02048308();
                func_020c1c20(data_ov000_022476f0.record);
                func_020c1cf4(2, data_ov000_022476fc, 0, -4);
                return 1;
            }
            func_020485b4(data_ov000_022476f0.lease);
        }
        func_020484dc(1, data_ov000_022476f0.handle);
    }
    return 0;
}
