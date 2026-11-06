typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u8 native_data_021cebe0[];
extern u8 native_data_021cebe2[];
extern u8 native_data_021cec60[];
extern u8 native_data_021ceca0[];
extern u8 native_data_021cecf4[];
extern u8 native_data_01fff940[];
extern u8 native_data_01fff94c[];
extern u8 native_data_01fff938[];
extern u8 native_data_01fff954[];
extern u8 native_data_01fff9a8[];
extern u8 native_data_01fff9b4[];
extern u8 native_data_01fff934[];
extern u8 native_data_01fff93c[];
extern u8 native_data_01fff944[];
extern u8 native_data_ov006_02217bd8[];
extern u8 native_data_01fffac0[];
extern u8 native_data_ov000_02246780[];

u32 native_itcm_01ff9fa0(void) {
    return *(u32 *)(native_data_021cebe0 + 0x30);
}
void native_itcm_01ff9ffc(void) {
    *(u32 *)(native_data_021cebe0 + 0x30) = 0;
}
u8 *native_itcm_01ffa010(void) {
    return native_data_021cebe2;
}
void native_itcm_01ffa01c(u32 value) {
    native_data_021cebe0[5] = value;
}
u8 *native_itcm_01ffa02c(void) {
    return native_data_021cebe0[5] == 0 ? native_data_021cec60 : native_data_021ceca0;
}
void native_itcm_01ffa348(u32 value) {
    *(u16 *)native_data_01fff940 = value;
}
void native_itcm_01ffa4a0(void) {
    *(u32 *)native_data_01fff94c = 0;
}
void native_itcm_01ffa8a8(u32 value) {
    native_data_021cebe0[6] = value;
}
void native_itcm_01ffa8b8(u32 value) {
    *(u32 *)(native_data_021cebe0 + 8) = value;
}
u32 native_itcm_01ffa8c8(void) {
    return *(u32 *)(native_data_021cebe0 + 8);
}
void native_itcm_01ffa968(u32 value) {
    native_data_01fff938[0] = value;
}
u32 native_itcm_01ffa978(void) {
    return native_data_01fff938[0];
}
void native_itcm_01ffae48(u32 first, u32 second) {
    *(u16 *)(native_data_01fff9a8 + 4) = first;
    *(u16 *)(native_data_01fff9a8 + 6) = second;
}
void native_itcm_01ffb324(u32 value) {
    *(u32 *)native_data_01fff954 = value;
}
u8 *native_itcm_01ffb334(void) {
    return native_data_01fff9a8;
}
u8 *native_itcm_01ffb340(void) {
    return native_data_01fff9b4;
}
int native_itcm_01ffb378(void) {
    return *(s8 *)(native_data_01fff9a8 + 8);
}
void native_itcm_01ffb388(u32 value) {
    native_data_01fff934[0] = value;
}
u8 *native_itcm_01ffb4ec(u32 index) {
    return native_data_021cecf4 + index * 0x170;
}
u8 *native_itcm_01ffb500(void) {
    return native_data_01fff93c;
}
u32 native_itcm_01ffb79c(void) {
    return *(u32 *)native_data_01fff944;
}
void native_ov006_021e2ee0(void) {
    *(u32 *)native_data_ov006_02217bd8 = 1;
}
void native_itcm_01ffb80c(void) {
}
void native_itcm_01ffb8a8(void) {
    *(u32 *)(native_data_021cebe0 + 0x1c) = 1;
}
u8 *native_itcm_01ffbb38(void) {
    return native_data_01fffac0;
}
void native_itcm_01ffc194(void) {
}
u32 native_itcm_01ffc2c0(void) {
    return 0;
}
u32 native_itcm_01ffc2c8(void) {
    return 0;
}
void native_itcm_01ffc2d0(void) {
}
u32 native_itcm_01ffc2d4(void) {
    return 0;
}
u32 native_itcm_01ffc324(void) {
    return 0x7fffff;
}
u8 *native_itcm_01fff264(u32 index) {
    return native_data_ov000_02246780 + index * 0x34;
}
