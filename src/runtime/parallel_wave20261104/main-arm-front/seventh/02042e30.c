#include "context.h"
u32 native_main_02042e30(u32 arg0, s32 *arg1, u32 *arg2) {
    u32 temp_r0;

    switch (arg0) {
    case 0:
        *arg1 = 0x19A;
        *arg2 = 0xF6;
        return 0xF6U;
    case 1:
        *arg1 = 0x267;
        *arg2 = 0x148;
        return 0x148U;
    case 2:
        *arg1 = 0x668;
        temp_r0 = 0x668U >> 2;
        *arg2 = temp_r0;
        return temp_r0;
    case 3:
        *arg1 = 0x802;
        *arg2 = 0x1EC;
        return 0x1ECU;
    case 4:
        *arg1 = 0xCD0;
        *arg2 = 0x267;
        return 0x267U;
    case 5:
        *arg1 = 0x1004;
        *arg2 = 0x2E2;
        return 0x2E2U;
    case 6:
        *arg1 = 0x1806;
        *arg2 = 0x4CE;
        return 0x4CEU;
    case 7:
        *arg1 = 0x4812;
        *arg2 = 0x668;
        return 0x668U;
    case 8:
        *arg1 = 0x5348;
        *arg2 = 0x802;
        return 0x802U;
    default:
        *arg1 = 0x19A;
        *arg2 = 0x19A;
        return 0x19AU;
    }
}
