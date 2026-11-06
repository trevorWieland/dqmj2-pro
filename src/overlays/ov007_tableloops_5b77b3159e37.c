typedef unsigned int u32;
typedef unsigned char u8;
typedef signed int s32;
typedef struct { u32 first; u32 second; u32 index; u32 prior; } Choice;
typedef struct { u32 words[36]; } Object;

extern u32 data_ov007_021da9dc[];
extern u32 data_02101ae8[];
extern void func_0204861c(u32, u32);
extern void func_0202a51c(u32);
extern void func_020485b4(u32);
extern void func_020484dc(u32, u32);
extern u32 func_ov007_021d873c(u32);
extern void func_02048a44(void *, u32);
extern void func_020485c8(u32, void *);
extern u32 func_ov007_021d8634(u32);
extern u32 func_ov007_021d864c(u32);
extern void func_02048a60(void *, u32, u32);
extern void func_02048a9c(void *, u32);
extern void func_02048a94(void *, u32);
extern void func_ov007_021d91f4(void);
extern void func_ov007_021d8d48(void);
extern Choice func_ov007_021d85e4(void);
extern void func_02048644(void *, u32, u32);
extern void func_ov007_021d9138(void);
extern u32 func_ov007_021d8664(u32);
extern u32 func_ov007_021d8828(u32);
extern u32 func_020c20e4(u32);

void native_ov007_021d8cc8(void) {
    if (data_ov007_021da9dc[7]) {
        func_0204861c(0, ((u8 *)data_ov007_021da9dc[7])[129]);
        func_0202a51c(data_ov007_021da9dc[7]);
    }
    if (data_ov007_021da9dc[1]) {
        func_0204861c(0, ((u8 *)data_ov007_021da9dc[1])[129]);
        func_0202a51c(data_ov007_021da9dc[10]);
    }
    if (data_ov007_021da9dc[9]) {
        func_020485b4(data_ov007_021da9dc[9]);
    }
    func_020484dc(0, ((u8 *)data_ov007_021da9dc)[0]);
}

void native_ov007_021d8db8(void) {
    s32 index;
    u32 first;
    u32 second;
    for (index = 0; index < 16; index++) {
        func_020485c8(1, &((Object *)data_ov007_021da9dc[3])[index]);
        first = func_ov007_021d8634(index);
        second = func_ov007_021d864c(index);
        func_02048a60(&((Object *)data_ov007_021da9dc[3])[index], first - 4, second - 4);
        func_02048a9c(&((Object *)data_ov007_021da9dc[3])[index], 0);
        func_02048a94(&((Object *)data_ov007_021da9dc[3])[index], 0);
    }
    func_ov007_021d91f4();
    func_ov007_021d8d48();
}

void native_ov007_021d9158(void) {
    Choice choice = func_ov007_021d85e4();
    func_02048a60((void *)data_ov007_021da9dc[2], choice.first - 4, choice.second - 4);
    func_ov007_021d9138();
    func_ov007_021d8d48();
    data_02101ae8[801] = 1;
}

void native_ov007_021d91f4(void) {
    s32 index;
    u32 mode;
    u32 type;
    for (index = 0; index < 16; index++) {
        mode = 15;
        type = func_ov007_021d8664(index);
        switch (type) {
            case 0:
                mode = 2;
                break;
            case 1:
                if (func_ov007_021d8828(index)) {
                    if (func_020c20e4(index) == 0) {
                        mode = 1;
                    } else {
                        mode = 21;
                    }
                } else {
                    mode = 13;
                }
                break;
            case 2:
                mode = 3;
                break;
        }
        func_02048644(&((Object *)data_ov007_021da9dc[3])[index], data_ov007_021da9dc[4], mode);
    }
}

void native_ov007_021d929c(void) {
    s32 index;
    u32 mode;
    u32 type;
    for (index = 0; index < 16; index++) {
        if (func_ov007_021d873c(index)) {
            mode = 15;
            type = func_ov007_021d8664(index);
            switch (type) {
                case 0:
                    mode = 16;
                    break;
                case 1:
                    mode = 15;
                    break;
                case 2:
                    mode = 17;
                    break;
            }
            func_02048644(&((Object *)data_ov007_021da9dc[3])[index], data_ov007_021da9dc[4], mode);
        }
    }
}

void native_ov007_021d932c(u32 index, u32 mode) {
    u32 enabled = (((Object *)data_ov007_021da9dc[3])[index].words[31] & 2) == 2;
    func_02048644(&((Object *)data_ov007_021da9dc[3])[index], data_ov007_021da9dc[4], mode);
    if (enabled) {
        ((Object *)data_ov007_021da9dc[3])[index].words[31] = ((Object *)data_ov007_021da9dc[3])[index].words[31] | 2;
    } else {
        ((Object *)data_ov007_021da9dc[3])[index].words[31] = ((Object *)data_ov007_021da9dc[3])[index].words[31] & ~2;
    }
}
