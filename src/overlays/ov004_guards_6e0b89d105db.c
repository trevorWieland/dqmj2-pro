typedef unsigned int u32;

extern u32 func_ov004_021d7cc4(void);
extern u32 func_ov004_021d7d00(void);
extern u32 func_ov004_021d7d3c(void);
extern u32 func_ov004_021d7d3c_alias1(void);
extern u32 func_ov004_021d7d78(void);
extern u32 func_ov004_021d7d78_alias1(void);
extern u32 func_ov004_021d82c8(void);
extern u32 func_ov004_021d8304(void);
extern u32 func_ov004_021d8920(void);
extern u32 func_ov004_021d895c(void);

u32 native_ov004_021d7304(u32 (*callback)(u32), u32 argument) {
    u32 *cursor;
    u32 total;
    u32 callbacks[32];
    callbacks[2] = 0;
    total= 0x30EB87;
    cursor = callbacks;
    callbacks[0] = (u32)(func_ov004_021d7d3c+0x1000)+0x320;
    callbacks[1] = (u32)(func_ov004_021d7d3c_alias1+0x1000)+0x320;
    do {
        total += ((u32 (*)(void))(*cursor - 0x1320))();
        cursor++;
    } while (*cursor);
    if (total % 241 != 0) {
        total = callback(argument);
    }
    return total;
}

u32 native_ov004_021d73a4(u32 (*callback)(u32), u32 argument) {
    u32 *cursor;
    u32 total;
    u32 callbacks[32];
    callbacks[2] = 0;
    total= 0x30EB87;
    cursor = callbacks;
    callbacks[0] = (u32)(func_ov004_021d7d78+0x1000)+0x320;
    callbacks[1] = (u32)(func_ov004_021d7d78_alias1+0x1000)+0x320;
    do {
        total += ((u32 (*)(void))(*cursor - 0x1320))();
        cursor++;
    } while (*cursor);
    if (total % 251 == 0) {
        total = callback(argument);
    }
    return total;
}

u32 native_ov004_021d7444(u32 (*callback)(u32), u32 argument) {
    u32 *cursor;
    u32 total;
    u32 callbacks[32];
    callbacks[2] = 0;
    total= 0x30EB87;
    cursor = callbacks;
    callbacks[0] = (u32)(func_ov004_021d82c8+0x1000)+0x320;
    callbacks[1] = (u32)(func_ov004_021d7cc4+0x1000)+0x320;
    do {
        total += ((u32 (*)(void))(*cursor - 0x1320))();
        cursor++;
    } while (*cursor);
    if (total % 241 != 0) {
        total = callback(argument);
    }
    return total;
}

u32 native_ov004_021d74e4(u32 (*callback)(u32), u32 argument) {
    u32 *cursor;
    u32 total;
    u32 callbacks[32];
    callbacks[2] = 0;
    total= 0x30EB87;
    cursor = callbacks;
    callbacks[0] = (u32)(func_ov004_021d8304+0x1000)+0x320;
    callbacks[1] = (u32)(func_ov004_021d7d00+0x1000)+0x320;
    do {
        total += ((u32 (*)(void))(*cursor - 0x1320))();
        cursor++;
    } while (*cursor);
    if (total % 251 == 0) {
        total = callback(argument);
    }
    return total;
}

u32 native_ov004_021d7584(u32 (*callback)(u32), u32 argument) {
    u32 *cursor;
    u32 total;
    u32 callbacks[32];
    total= 0x30EB87;
    cursor = callbacks;
    callbacks[0] = (u32)(func_ov004_021d8920+0x1000)+0x320;
    callbacks[1] = 0;
    do {
        total += ((u32 (*)(void))(*cursor - 0x1320))();
        cursor++;
    } while (*cursor);
    if (total % 241 != 0) {
        total = callback(argument);
    }
    return total;
}

u32 native_ov004_021d7614(u32 (*callback)(u32), u32 argument) {
    u32 *cursor;
    u32 total;
    u32 callbacks[32];
    total= 0x30EB87;
    cursor = callbacks;
    callbacks[0] = (u32)(func_ov004_021d895c+0x1000)+0x320;
    callbacks[1] = 0;
    do {
        total += ((u32 (*)(void))(*cursor - 0x1320))();
        cursor++;
    } while (*cursor);
    if (total % 251 == 0) {
        total = callback(argument);
    }
    return total;
}
