typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_ov001_021e3db0();
u32 native_ov001_021e3eec(void *arg0, u32 arg1) {
    void *record = M2C_FIELD(arg0, void **, 0x1E8);
    if (M2C_FIELD(record, u8 *, 0xB1) != 0) goto done;
    if (M2C_FIELD(record, u16 *, 0xC6) != 0 && native_fn_ov001_021e3db0(M2C_FIELD(record, u8 *, 0xC8), arg1, 1))
        return M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), u16 *, 0xC6);
    record = M2C_FIELD(arg0, void **, 0x1E8);
    if (M2C_FIELD(record, u16 *, 0xCA) != 0 && native_fn_ov001_021e3db0(M2C_FIELD(record, u8 *, 0xCC), arg1, 0))
        return M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), u16 *, 0xCA);
 done:
    return 0;
}
