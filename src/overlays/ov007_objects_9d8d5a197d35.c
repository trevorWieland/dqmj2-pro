typedef unsigned char u8;
typedef unsigned int u32;

extern volatile u32 data_ov007_021da9d8[];
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

void native_ov007_021d88dc(u32 index) {
    u32 *object = (u32 *)data_ov007_021da9d8[index];
    object[6] = object[6] | 2;
    func_02086b14((void *)data_ov007_021da9d8[index], 16);
}

void native_ov007_021d8944(u32 index, u32 first, u32 second) {
    func_02086ad8((void *)data_ov007_021da9d8[index]);
    func_02085284((u8 *)data_ov007_021da9d8[index] + 60, 6, first, second);
}

u32 native_ov007_021d8984(u32 index) {
    return (((u32 *)data_ov007_021da9d8[index])[6] & 2) != 2;
}

void native_ov007_021d89a8(void) {
    void (*target)(void *) = func_02084f4c;
    target((void *)data_ov007_021da9d8[0]);
}

void native_ov007_021d8abc(u32 enabled) {
    if (enabled != 0) {
        ((u32 *)data_ov007_021da9dc[7])[31] = ((u32 *)data_ov007_021da9dc[7])[31] | 2;
    } else {
        ((u32 *)data_ov007_021da9dc[7])[31] = ((u32 *)data_ov007_021da9dc[7])[31] & ~2;
    }
}

void native_ov007_021d9138(void) {
    void (*target)(void *, u32) = func_02048a44;
    target((u8 *)data_ov007_021da9dc[2] + 8, 1);
}

void native_ov007_021d91b8(u32 enabled) {
    if (enabled != 0) {
        ((u32 *)data_ov007_021da9dc[2])[31] = ((u32 *)data_ov007_021da9dc[2])[31] | 2;
    } else {
        ((u32 *)data_ov007_021da9dc[2])[31] = ((u32 *)data_ov007_021da9dc[2])[31] & ~2;
    }
}

void native_ov007_021d93ac(u32 kind, u32 enabled) {
    u32 *object;
    if (kind == 0) {
        object = (u32 *)data_ov007_021da9dc[1];
    } else {
        object = (u32 *)data_ov007_021da9dc[10];
    }
    if (enabled != 0) {
        object[31] = object[31] | 2;
    } else {
        object[31] = object[31] & ~2;
    }
}

void native_ov007_021d93dc(u32 kind, u32 first, u32 second) {
    void *object;
    if (kind == 0) {
        object = (void *)data_ov007_021da9dc[1];
    } else {
        object = (void *)data_ov007_021da9dc[10];
    }
    func_02048a60(object, first, second);
}

void native_ov007_021d9400(u32 kind, u32 first, u32 second) {
    void *object;
    if (kind == 0) {
        object = (void *)data_ov007_021da9dc[1];
    } else {
        object = (void *)data_ov007_021da9dc[10];
    }
    func_02048a88(object, first, second);
}

void native_ov007_021d953c(void) {
    data_ov007_021da9dc[11] = func_0202a44c(5, 144, 4);
    func_020485c8(1, data_ov007_021da9dc[11]);
}

void native_ov007_021d956c(void) {
    if (data_ov007_021da9dc[11] != 0) {
        func_0204861c(1, ((u8 *)data_ov007_021da9dc[11])[129]);
        func_0202a498(5, data_ov007_021da9dc[11]);
        data_ov007_021da9dc[11] = 0;
    }
}

void native_ov007_021d95b0(u32 first, u32 second) {
    func_02048644(data_ov007_021da9dc[11], data_ov007_021da9dc[8], 0);
    func_02048a60((void *)data_ov007_021da9dc[11], first - 4, second - 4);
}

void native_ov007_021d95ec(void) {
    u32 *object = (u32 *)data_ov007_021da9dc[11];
    if ((object[31] & 2) == 2) {
        func_02048a44((u8 *)object + 8, 1);
    }
}
