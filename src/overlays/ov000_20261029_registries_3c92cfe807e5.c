typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

typedef struct {
    u32 id;
    u8 payload[20];
} Row24;

typedef struct {
    u32 id;
    u8 payload[44];
} Row48;

extern Row48 data_ov000_02231f64[16];
extern Row24 data_ov000_02231e44[12];
extern Row24 data_ov000_02231c04[12];
extern Row24 data_ov000_02231d24[12];

u32 native_ov000_021df544(u32 id) {
    s32 index;
    Row48 *row;
    row = data_ov000_02231f64;
    index = 0;
    do {
        if (id == row->id) {
            return 1;
        }
        index++;
        row++;
    } while (index < 16);
    return 0;
}

s32 native_ov000_021df578(void) {
    s32 index;
    Row48 *row;
    row = data_ov000_02231f64;
    index = 0;
    do {
        if (row->id == 0) {
            return index;
        }
        index++;
        row++;
    } while (index < 16);
    return -1;
}

u8 *native_ov000_021df5a8(u32 id) {
    s32 index;
    u8 *result;
    Row48 *row;
    result = 0;
    row = data_ov000_02231f64;
    index = 0;
    do {
        if (id == row->id) {
            result = data_ov000_02231f64[index].payload;
            break;
        }
        index++;
        row++;
    } while (index < 16);
    return result;
}

u32 native_ov000_021df5f0(u32 id) {
    s32 index;
    Row24 *row;
    row = data_ov000_02231e44;
    index = 0;
    do {
        if (id == row->id) {
            return 1;
        }
        index++;
        row++;
    } while (index < 12);
    return 0;
}

s32 native_ov000_021df624(void) {
    s32 index;
    Row24 *row;
    row = data_ov000_02231e44;
    index = 0;
    do {
        if (row->id == 0) {
            return index;
        }
        index++;
        row++;
    } while (index < 12);
    return -1;
}

u8 *native_ov000_021df654(u32 id) {
    s32 index;
    u8 *result;
    Row24 *row;
    result = 0;
    row = data_ov000_02231e44;
    index = 0;
    do {
        if (id == row->id) {
            result = data_ov000_02231e44[index].payload;
            break;
        }
        index++;
        row++;
    } while (index < 12);
    return result;
}

u32 native_ov000_021df69c(u32 id) {
    s32 index;
    Row24 *row;
    row = data_ov000_02231c04;
    index = 0;
    do {
        if (id == row->id) {
            return 1;
        }
        index++;
        row++;
    } while (index < 12);
    return 0;
}

s32 native_ov000_021df6d0(void) {
    s32 index;
    Row24 *row;
    row = data_ov000_02231c04;
    index = 0;
    do {
        if (row->id == 0) {
            return index;
        }
        index++;
        row++;
    } while (index < 12);
    return -1;
}

u8 *native_ov000_021df700(u32 id) {
    s32 index;
    u8 *result;
    Row24 *row;
    result = 0;
    row = data_ov000_02231c04;
    index = 0;
    do {
        if (id == row->id) {
            result = data_ov000_02231c04[index].payload;
            break;
        }
        index++;
        row++;
    } while (index < 12);
    return result;
}

u32 native_ov000_021df748(u32 id) {
    s32 index;
    Row24 *row;
    row = data_ov000_02231d24;
    index = 0;
    do {
        if (id == row->id) {
            return 1;
        }
        index++;
        row++;
    } while (index < 12);
    return 0;
}

s32 native_ov000_021df77c(void) {
    s32 index;
    Row24 *row;
    row = data_ov000_02231d24;
    index = 0;
    do {
        if (row->id == 0) {
            return index;
        }
        index++;
        row++;
    } while (index < 12);
    return -1;
}

u8 *native_ov000_021df7ac(u32 id) {
    s32 index;
    u8 *result;
    Row24 *row;
    result = 0;
    row = data_ov000_02231d24;
    index = 0;
    do {
        if (id == row->id) {
            result = data_ov000_02231d24[index].payload;
            break;
        }
        index++;
        row++;
    } while (index < 12);
    return result;
}

