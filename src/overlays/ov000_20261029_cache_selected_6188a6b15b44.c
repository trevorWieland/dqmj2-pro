typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Lease;
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_02048308(void);
extern void func_0204b1a0(void *);
typedef struct { u8 reserved[8]; void *record; u8 gap[12]; Lease *lease; } State;
extern State data_ov000_0224532c;
extern u8 data_ov000_0222f918[];
void native_ov000_022159b8(const char *name, u32 kind) {
    data_ov000_0222f918[0] = func_02048404(1, name, kind, 2);
    data_ov000_0224532c.lease = func_0204854c(1, data_ov000_0222f918[0]);
    data_ov000_0224532c.record = data_ov000_0224532c.lease->record;
    func_02048308();
    func_0204b1a0(data_ov000_0224532c.record);
}
