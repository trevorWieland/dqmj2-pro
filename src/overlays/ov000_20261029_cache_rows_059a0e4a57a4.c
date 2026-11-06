typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
extern u32 func_0203cfe0();
extern u32 func_02048308();
extern u8 func_02048404(u32, const char *, u32, u32);
extern void func_020484dc(u32, u32);
typedef struct { u32 flags; void *record; } Lease;
extern Lease *func_0204854c(u32, u32);
extern void func_020485b4(Lease *);
extern void func_0204b1a0();
extern void func_020c1c20(void *);
extern void func_020c1c30(u32, void *, u8, u32, int);
extern void func_020c1de0(u32, void *, u32, u32, u32, u32);
extern u32 data_02101ae8[];
extern u8 data_ov000_0222fb20[];
extern u8 data_ov000_0222fb28[];
extern u8 data_ov000_0222fb34[];
typedef struct { u8 reserved; u8 handle; u8 padding[2]; Lease *lease; u32 gap[2]; void *record; } State;
extern State data_ov000_02246318;
extern u8 data_ov000_0224632c[];
extern u8 data_ov000_02246348[];
extern u8 data_ov000_0224636c[];
extern u8 data_ov000_02246370[];
extern u8 data_ov000_02246374[];
extern u8 data_ov000_02246378[];
u32 native_ov000_0221d474(void) {
    Lease *temp_r0_2;
    u8 temp_r0;
    void *temp_r2;
    u32 var_r3;
    s32 var_r7;
    s32 var_r8_2;
    u8 *var_r8;
    s32 var_r9;
    s32 var_r9_2;
    u8 *var_r9_3;
    s32 var_r10;

    temp_r0 = func_02048404(1U, (s8 *) data_ov000_0222fb34, 4U, 2U);
    data_ov000_02246318.handle = temp_r0;
    if (temp_r0 != 0xFF) {
        temp_r0_2 = func_0204854c(1U, (u32) temp_r0);
        data_ov000_02246318.lease = temp_r0_2;
        if (temp_r0_2 != 0) {
            temp_r2 = temp_r0_2->record;
            data_ov000_02246318.record = temp_r2;
            if (temp_r2 != 0) {
                func_020c1c20(temp_r2);
                var_r7 = 0;
                var_r8 = data_ov000_02246348;
                do {
                    func_020c1c30(2, var_r8, 0x1CU, 0, 2);
                    var_r7 += 1;
                    var_r8 += 4;
                } while (var_r7 < 5);
                var_r8_2 = 0;
                do {
                    func_020c1c30(2, data_ov000_02246348 + ((var_r8_2 + 5) * 4), 0x1DU, 0, 2);
                    var_r8_2 += 1;
                } while (var_r8_2 < 4);
                func_020c1c30(2, data_ov000_0224636c, 0x1FU, 0, 2);
                func_020c1c30(2, data_ov000_02246370, 0x1EU, 0, 2);
                func_020c1c30(2, data_ov000_02246374, 0x15U, 0, 2);
                func_020c1c30(2, data_ov000_02246378, 0x16U, 0, 2);
                var_r9 = 0;
                do {
                    func_020c1c30(2, data_ov000_02246348 + ((var_r9 + 0xD) * 4), data_ov000_0222fb28[2], 0, -3);
                    var_r9 += 1;
                } while (var_r9 < 3);
                var_r9_2 = 0;
                do {
                    func_020c1c30(2, data_ov000_02246348 + ((var_r9_2 + 0x10) * 4), data_ov000_0222fb20[func_0203cfe0()], 0, -3);
                    var_r9_2 += 1;
                } while (var_r9_2 < 6);
                data_02101ae8[0x321] = 1;
                func_02048308();
                func_0204b1a0(data_ov000_02246318.record);
                var_r10 = 0;
                var_r9_3 = data_ov000_0224632c;
                do {
                    if (var_r10 == 0) {
                        var_r3 = 0x24;
                    } else {
                        var_r3 = 0x26;
                    }
                    func_020c1de0(2, var_r9_3, 0, (u8) var_r3, 0, 0x20);
                    var_r10 += 1;
                    var_r9_3 += 4;
                } while (var_r10 < 5);
                return 1U;
            }
            func_020485b4(data_ov000_02246318.lease);
        }
        func_020484dc(1, data_ov000_02246318.handle);
    }
    return 0U;
}
