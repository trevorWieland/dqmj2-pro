typedef unsigned int u32;

u32 native_ov004_021d7240(void (*callback)(void)) {
    if (callback != 0) {
        callback();
    }
    return ~(u32)callback;
}

void native_ov004_021d7258(void) {
}

void native_ov004_021d7300(void) {
}
