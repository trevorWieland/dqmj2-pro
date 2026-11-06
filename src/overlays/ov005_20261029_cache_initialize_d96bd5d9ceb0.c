typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Lease;
typedef struct {
    u8 reserved[24];
    Lease *lease;
    u8 gap[56];
    void *record;
} State;
extern State data_ov005_021e9818;
extern u8 data_ov005_021e708c[];
extern void func_020489f0(u32);
extern void func_02008c58(u32, void *, u32);
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_02048308(void);

void native_ov005_021ddd60(const char *name, u32 kind) {
    func_020489f0(0);
    *(volatile u32 *)0x04000000 = (*(volatile u32 *)0x04000000 & 0xFFCFFFEF) | 0x10;
    func_02008c58(0, (void *)0x06400000, 0x40000);
    data_ov005_021e708c[0] = func_02048404(0, name, kind, 2);
    data_ov005_021e9818.lease = func_0204854c(0, data_ov005_021e708c[0]);
    data_ov005_021e9818.record = data_ov005_021e9818.lease->record;
    func_02048308();
}
