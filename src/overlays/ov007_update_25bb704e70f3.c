typedef unsigned char u8;
typedef unsigned int u32;

extern u32 data_ov007_021da0f4[];
extern u32 func_ov007_021d7ab0(void);
extern u32 func_ov007_021d9040(void);
extern void func_02008430(void);
extern void func_ov007_021d8abc(u32);
extern void func_ov007_021d91b8(u32);
extern u32 func_ov007_021d873c(u32);
extern void func_ov007_021d80b0(void);
extern u32 func_ov007_021d7c5c(void);
extern void func_020c2020(void);
extern void func_ov007_021d91f4(void);
extern u32 func_ov007_021d8694(u32);
extern void func_ov007_021d8944(u32, u32, u32);
extern u32 func_ov007_021d7ac0(void);
extern u32 func_02041944(void);
extern u32 func_02041814(void);
extern void func_ov007_021d7d7c(void);
extern u32 func_020725b8(void);
extern u32 func_ov007_021d8634(u32);
extern u32 func_ov007_021d864c(u32);
extern void func_ov007_021d9ccc(u32, u32, u32, u32, u32);
extern void func_ov007_021d9e68(void);
extern u32 func_ov007_021d82d8(void);
extern u32 func_ov007_021d96b0(u32);
extern void func_ov007_021d7ad0(u32);
extern u32 func_ov007_021d81d0(void);
extern void func_ov007_021d8908(u32);
extern u32 func_020273c8(void);
extern u32 func_ov007_021da04c(void);
extern u32 func_ov007_021d9c3c(void);
extern void func_ov007_021d956c(void);
extern void func_ov007_021d7c4c(void);
extern void func_0204176c(void);
extern void func_ov007_021d7c58(void);

u32 native_ov007_021d837c(void) {
    u32 first;
    u32 second;
    switch (func_ov007_021d7ab0()) {
        case 0:
            if (func_ov007_021d9040() == 0) {
                func_02008430();
            }
            if (data_ov007_021da0f4[2] == 0) {
                func_ov007_021d8abc(0);
            }
            func_ov007_021d91b8(0);
            break;
        case 1:
            if (func_ov007_021d873c(data_ov007_021da0f4[2]) == 0) {
                func_ov007_021d80b0();
            }
            if (func_ov007_021d7c5c() == 0) {
                func_02008430();
            }
            func_020c2020();
            func_ov007_021d91f4();
            break;
        case 2:
            func_ov007_021d8944(0, 0, func_ov007_021d8694(data_ov007_021da0f4[2]));
            break;
        case 5:
            if (func_ov007_021d7ac0() == 0) {
                if (func_02041944() && func_02041814() != 1) {
                    func_ov007_021d7d7c();
                    first = func_ov007_021d8634(func_020725b8());
                    second = func_ov007_021d864c(func_020725b8());
                    func_ov007_021d9ccc(1, 0, 30, (u8)first, (u8)second);
                }
            } else if (func_ov007_021d7ac0() == 4) {
                func_ov007_021d9e68();
            }
            break;
        case 6:
            func_ov007_021d91b8(1);
            if (func_ov007_021d82d8()) {
                if (func_ov007_021d96b0(140)) {
                    func_ov007_021d7ad0(9);
                } else {
                    func_ov007_021d7ad0(7);
                }
            } else if (func_ov007_021d81d0()) {
                func_ov007_021d8908(0);
                func_ov007_021d7ad0(8);
            }
            break;
        case 7:
            if (func_ov007_021d7ac0() == 0) {
                first = func_ov007_021d8634(data_ov007_021da0f4[2]);
                second = func_ov007_021d864c(data_ov007_021da0f4[2]);
                func_ov007_021d9ccc(1, 1, 30, (u8)first, (u8)second);
            } else if (func_ov007_021d7ac0() == 2) {
                func_ov007_021d9e68();
            }
            if (func_020273c8() != 5) {
                return 12;
            }
            break;
        case 10:
            if (func_ov007_021da04c() && func_ov007_021d9c3c()) {
                func_ov007_021d7ad0(4);
                func_ov007_021d956c();
            }
            break;
    }
    func_ov007_021d7c4c();
    func_0204176c();
    func_ov007_021d7c58();
    return 5;
}
