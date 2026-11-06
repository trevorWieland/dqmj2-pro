typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Lease;
typedef struct { u8 reserved[32]; Lease *lease; void *record; } State;
extern State data_ov001_02239c10;
extern const char data_ov001_0222ee38[];
extern u8 data_ov001_0222ed34[];
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_0204b1a0(void *);
extern void func_02048308(void);
void native_ov001_021fc908(void) {
    data_ov001_0222ed34[0] = func_02048404(1, data_ov001_0222ee38, 4, 2);
    data_ov001_02239c10.lease = func_0204854c(1, data_ov001_0222ed34[0]);
    data_ov001_02239c10.record = data_ov001_02239c10.lease->record;
    
    func_0204b1a0(data_ov001_02239c10.record);
}
