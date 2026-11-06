typedef unsigned char u8;
typedef unsigned int u32;

extern u32 data_ov007_021da9d8[];
extern u32 data_ov007_021da9dc[];
extern void func_02086b14(void *, u32);
extern void func_020850a0(void *);
extern void func_02086ad8(void *);
extern void func_02085284(void *, u32, u32, u32);
extern void func_02084f4c(void *);
extern void func_02048a44(void *, u32);
extern void func_02048a60(void *, u32, u32);
extern void func_02048a88(void *, u32, u32);
extern u32 func_0202a44c(u32, u32, u32);
extern void func_020485c8(u32, u32);
extern void func_0204861c(u32, u32);
extern void func_0202a498(u32, u32);
extern void func_02048644(u32, u32, u32);

void native_ov007_021d8908(u32 index) {
    func_020850a0((void *)data_ov007_021da9d8[index]);
    ((u32 *)data_ov007_021da9d8[index])[6] = ((u32 *)data_ov007_021da9d8[index])[6] & ~2;
}
