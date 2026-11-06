typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;

typedef struct { u32 value; u8 reserved[44]; } Word48;
typedef struct { u16 value; u8 reserved[46]; } Half48;
typedef struct { u8 value; u8 reserved[47]; } Byte48;
typedef struct { u32 value; u32 reserved[2]; } Word12;

extern Word48 data_ov007_021da5ec[];
extern Word48 data_ov007_021da5f0[];
extern Word48 data_ov007_021da5f4[];
extern Half48 data_ov007_021da5f8[];
extern Half48 data_ov007_021da5fa[];
extern Byte48 data_ov007_021da5fc[];
extern Byte48 data_ov007_021da610[];
extern Word12 data_ov007_021da534[];
extern Word12 data_ov007_021da538[];
extern Word12 data_ov007_021da53c[];
extern Byte48 data_ov007_021da614[];
extern Byte48 data_ov007_021da614[];
extern Half48 data_ov007_021da612[];
extern s8 data_ov007_021da06c[];

u32 native_ov007_021d8634(u32 index) {
    return data_ov007_021da5ec[index].value;
}

u32 native_ov007_021d864c(u32 index) {
    return data_ov007_021da5f0[index].value;
}

u32 native_ov007_021d8664(u32 index) {
    return data_ov007_021da5f4[index].value;
}

u32 native_ov007_021d867c(u32 index) {
    return data_ov007_021da5f8[index].value;
}

u32 native_ov007_021d8694(u32 index) {
    return data_ov007_021da5fa[index].value;
}

u32 native_ov007_021d86ac(u32 index) {
    return data_ov007_021da5fc[index].value;
}

u32 native_ov007_021d86c4(u32 index) {
    return data_ov007_021da610[index].value;
}

u32 native_ov007_021d86dc(u32 index) {
    return data_ov007_021da534[index].value;
}

u32 native_ov007_021d86f4(u32 index) {
    return data_ov007_021da538[index].value;
}

u32 native_ov007_021d870c(u32 index) {
    return data_ov007_021da53c[index].value;
}

u32 native_ov007_021d873c(u32 index) {
    return data_ov007_021da614[index].value;
}

void native_ov007_021d8724(u32 index, u32 value) {
    data_ov007_021da614[index].value = value;
}

void native_ov007_021d8754(u32 index, u32 value) {
    data_ov007_021da612[index].value = value;
}

s32 native_ov007_021d8838(u32 index) {
    return data_ov007_021da06c[index];
}
