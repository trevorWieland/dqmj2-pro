typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Lease;
typedef struct { u8 reserved[28]; void *record; u8 gap[12]; Lease *lease; } State;
extern State data_ov005_021ed234;
extern const char data_ov005_021e7738[];
extern u8 data_ov005_021e74a8[];
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_0204b1a0(void *);
extern void func_02048308(void);
void native_ov005_021e0ab0(void) {
    data_ov005_021e74a8[0] = func_02048404(1, data_ov005_021e7738, 4, 2);
    data_ov005_021ed234.lease = func_0204854c(1, data_ov005_021e74a8[0]);
    data_ov005_021ed234.record = data_ov005_021ed234.lease->record;
    func_02048308();
    func_0204b1a0(data_ov005_021ed234.record);
}
