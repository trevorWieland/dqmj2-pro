typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 first; u32 second; u32 index; u32 prior; } Choice;

extern u32 data_ov007_021da9dc[];
extern u8 data_ov007_021da8e8[];
extern u32 data_020feae8[];
extern Choice func_ov007_021d85e4(void);
extern u32 func_ov007_021d85fc(void);
extern u32 func_020c20e4(u32);
extern void func_020485c8(u32, void *);
extern u32 func_ov007_021d860c(void);
extern void func_02048644(void *, u32, u32);
extern void func_02048a60(void *, u32, u32);
extern void func_02048a9c(void *, u32);
extern void func_02048a94(void *, u32);
extern u32 func_02048404(u32, void *, u32, u32);
extern u32 func_0204854c(u32);
extern u32 func_0202a474(u32, u32);
extern void func_ov007_021d89c0(void);
extern void func_ov007_021d8fbc(u32);
extern void func_02048308(void);
extern void func_020485b4(u32);
extern void func_020484dc(u32, u32);
extern void func_ov007_021d8abc(u32);

void native_ov007_021d8bc0(void) {
    Choice choice = func_ov007_021d85e4();
    u32 available;
    u8 mode;
    u32 skipped = 0;
    if ((((u32 *)data_ov007_021da9dc[7])[31] & 2) == 2) {
        available = func_020c20e4(func_ov007_021d85fc());
        if (func_ov007_021d860c() < 10800) {
            if (choice.index == 3) {
                if (available) {
                    mode = 19;
                } else {
                    func_ov007_021d8abc(0);
                    skipped = 1;
                }
            } else {
                if (available) {
                    mode = available + 5;
                } else {
                    func_ov007_021d8abc(0);
                    skipped = 1;
                }
            }
        } else {
            if (choice.index == 3) {
                if (available == 0) {
                    mode = 9;
                } else {
                    mode = 20;
                }
            } else {
                if (available == 0) {
                    mode = 9;
                } else {
                    mode = available + 9;
                }
            }
        }
        if (skipped == 0) {
            func_02048644((void *)data_ov007_021da9dc[7], data_ov007_021da9dc[8], mode);
        }
    }
    data_020feae8[336] = 1;
}
