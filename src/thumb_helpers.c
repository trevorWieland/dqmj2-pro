typedef unsigned int u32;

extern volatile u32 data_021cfcf8[];
extern volatile u32 data_020e33e4[];
extern volatile u32 data_021d1540[];

void native_main_0208b8fc(void) {
}

u32 native_main_0208b900(void) {
    return 1;
}

void native_main_0208baa0(u32 value) {
    data_021cfcf8[15] = value;
}

void native_main_0208d744(u32 value) {
    ((volatile u32 *)data_020e33e4[1])[41] = value;
}

void native_main_0208d754(void) {
    ((volatile u32 *)data_020e33e4[1])[41] = 0;
}

void native_main_0208d7f8(volatile u32 *target) {
    target[41] = ((volatile u32 *)data_020e33e4[1])[41];
}

void native_main_0208eb10(void) {
    data_021d1540[2] |= 2;
}

u32 native_main_0208ec10(volatile u32 *value) {
    u32 first = value[25];
    if (first == 0) {
        first = value[26];
    }
    return first;
}
