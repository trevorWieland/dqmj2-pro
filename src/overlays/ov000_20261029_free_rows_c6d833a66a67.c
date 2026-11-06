typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

typedef struct {
    u16 key;
    u8 field_2;
    u8 field_3;
    u8 payload[16];
} Row20;

typedef struct {
    u8 key;
    u8 payload[15];
} Row16;

typedef struct {
    u8 key;
    u8 payload[31];
} Row32;

typedef struct {
    u8 key;
    u8 payload[63];
} Row64;

extern Row20 data_ov000_02232868[32];
extern Row64 data_ov000_022332e8[32];
extern Row32 data_ov000_02232ae8[64];
extern Row16 data_ov000_02232668[32];
extern s16 data_ov000_0222ebf4;
extern u8 data_ov000_02234388[];

u8 *native_ov000_021e54f4(void) {
    s32 index;
    Row20 *row;
    u8 *result;
    result = 0;
    row = data_ov000_02232868;
    index = 0;
    do {
        if (row->key == 0) {
            result = (u8 *)row;
            break;
        }
        index++;
        row++;
    } while (index < 32);
    return result;
}

u8 *native_ov000_021e57f8(void) {
    s32 index;
    Row64 *row;
    u8 *result;
    result = 0;
    row = data_ov000_022332e8;
    index = 0;
    do {
        if (row->key == 0) {
            result = (u8 *)row;
            break;
        }
        index++;
        row++;
    } while (index < 32);
    return result;
}

u8 *native_ov000_021e5c10(void) {
    s32 index;
    Row32 *row;
    u8 *result;
    result = 0;
    row = data_ov000_02232ae8;
    index = 0;
    do {
        if (row->key == 0) {
            result = (u8 *)row;
            break;
        }
        index++;
        row++;
    } while (index < 64);
    return result;
}

u8 *native_ov000_021e5fc8(void) {
    s32 index;
    Row16 *row;
    u8 *result;
    result = 0;
    row = data_ov000_02232668;
    index = 0;
    do {
        if (row->key == 0) {
            result = (u8 *)row;
            break;
        }
        index++;
        row++;
    } while (index < 32);
    return result;
}
