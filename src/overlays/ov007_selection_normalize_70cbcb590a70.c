typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;

extern u32 data_ov007_021da0f4[];
extern u32 func_ov007_021d873c(u32);
extern u32 func_ov007_021d8634(u32);
extern u32 func_ov007_021d864c(u32);
extern u32 func_ov007_021d867c(u32);
extern void func_ov007_021d7aa0(u32);
extern s32 func_ov007_021d7e1c(u32);
extern u16 *func_0202a634(void);
extern u32 func_ov007_021d8170(void);
extern void func_ov007_021d9628(u32);
extern s32 func_ov007_021d86ac(u32);
extern void func_0205be34(u32);
extern void func_0205bdfc(u32);
extern void func_020c20f4(u32);
extern void func_0205bf2c(u32);
extern u32 func_ov007_021d86c4(u32);
extern void func_0205c060(u32);
extern void func_020c211c(u32);
extern s32 func_ov007_021d876c(u32);
extern void func_0203d0d8(u32, u32);

void native_ov007_021d80b0(void) {
    u32 changed = 1;
    switch (data_ov007_021da0f4[2]) {
        case 9:
            data_ov007_021da0f4[2] = 0;
            break;
        case 10:
            data_ov007_021da0f4[2] = 0;
            break;
        case 11:
            data_ov007_021da0f4[2] = 0;
            break;
        case 12:
            data_ov007_021da0f4[2] = 0;
            break;
        default:
            changed = 0;
    }
    if (changed && func_ov007_021d873c(data_ov007_021da0f4[2]) == 0) {
        data_ov007_021da0f4[2] = 14;
    }
    data_ov007_021da0f4[0] = func_ov007_021d8634(data_ov007_021da0f4[2]);
    data_ov007_021da0f4[1] = func_ov007_021d864c(data_ov007_021da0f4[2]);
    func_ov007_021d7aa0(func_ov007_021d867c(data_ov007_021da0f4[2]));
}
