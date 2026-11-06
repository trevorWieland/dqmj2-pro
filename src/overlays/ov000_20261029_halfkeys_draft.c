typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;

typedef struct {
    u16 key;
    u8 field_2;
    u8 field_3;
    u8 payload[16];
} Row20;

extern Row20 data_ov000_02232868[32];

u32 native_ov000_021e5594(u32 raw_key) {
    s32 index;
    u32 count;
    Row20 *row;
    u8 key;
    count = 0;
    key = (u8)raw_key;
    row = data_ov000_02232868;
    index = 0;
    do {
        index++;
        if (row->key == key) {
            row->key = 0;
            count++;
        }
        row++;
    } while (index < 32);
    return count;
}

u8 *native_ov000_021e5744(u32 raw_key) {
    Row20 *row;
    u8 key;
    s32 index;
    row = data_ov000_02232868;
    key = (u8)raw_key;
    index = 0;
    do {
        if (row->key == key) {
            return row->payload;
        }
        index++;
        row++;
    } while (index < 32);
    return 0;
}

u32 native_ov000_021e577c(u32 raw_key, u32 value) {
    Row20 *row;
    u8 key;
    s32 index;
    u16 last;
    row = data_ov000_02232868;
    key = (u8)raw_key;
    index = 0;
    do {
        last = row->key;
        index++;
        if (last == key) {
            row->field_3 = (u8)value;
        }
        row++;
    } while (index < 32);
    return last;
}
