typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u8 native_data_021cebe0[];
extern u8 native_data_021ceb54[];
extern u8 native_data_021cec40[];
extern u8 native_data_01fff9a8[];
extern u8 native_data_01fff944[];
extern u8 native_data_021d4100[];
extern u8 *native_fn_ov000_02223c60(void);
extern u32 native_fn_02041814(void);
extern void native_fn_02027410(u32);
extern void native_fn_ov001_021fc95c(void);
extern void native_fn_ov001_021fcf58(void);
extern u32 native_fn_020841d0(void);
extern u32 native_fn_020841e8(void);
extern void native_fn_02084708(u8 *, u32);
extern u32 native_fn_020125bc(void);
extern void native_fn_020841f4(u32, u32);
extern u32 native_fn_020846bc(void);
extern u32 native_fn_020843e4(void);
extern u8 *native_fn_020844d0(void);
extern u8 *native_fn_01ffa02c(void);
extern void native_fn_02084434(u32);
extern void native_fn_02084474(u32);
extern void native_fn_0204bb08(u32);
extern void native_fn_02084180(u32);
extern void native_fn_020841b8(void);
extern void native_fn_01ffa22c(void);
extern u32 native_fn_020ba9d0(void);
extern u32 native_fn_02084568(void);
extern u32 native_fn_01ffa358(void);
extern u32 native_fn_01ffa8f0(int);
extern u8 *native_fn_01ffb4ec(u32);
extern void native_fn_01ffae9c(u32, u32, u32, u32);
extern void native_fn_02049e0c(u8);
extern void native_fn_020414c8(u32);
extern void native_fn_02049b84(u32);
extern void native_fn_01ffb060(u32);
extern void native_fn_020897ec(u32);
extern void native_fn_01ffaf98(void);
extern void native_fn_02048f7c(u32);
extern void native_fn_0204607c(void);
extern u8 *native_fn_02049ae4(void);
extern u8 *native_fn_01ffb340(void);
extern void native_fn_01ffb158(u32, u16);
extern u32 native_fn_0202a634(void);
extern u32 native_fn_ov000_0221794c(u8 *);
extern void native_fn_01ffb46c(void);
extern void native_fn_02049604(u8 *, u32);
extern void native_fn_01ffb530(u32, u32, u32, u32, u32, u32);
extern u8 **native_fn_02061dcc(int);
extern void native_fn_02049ffc(u32);
extern u32 native_fn_0205e644(u32);
extern void native_fn_0205e66c(u32);
extern void native_fn_0205e73c(u32);
extern void native_fn_0205e7a8(u32, u32);
extern u8 *native_fn_ov000_02223c54(void);
extern u32 native_fn_020b9f84(void (*)(void));
extern void native_fn_01ffb744(void);
extern void native_fn_020414b0(u32);
extern void native_fn_01ffb8a8(void);
extern u32 native_fn_020bb144(u32);

void native_ov001_021fc62c(void) {
    native_fn_ov001_021fc95c();
    native_fn_ov001_021fcf58();
}
u32 native_itcm_01ff97a0(void) {
    u32 result = *(u32 *)native_fn_ov000_02223c60();
    if (native_fn_02041814() == 1) return result;
    result = *(u32 *)(native_data_021ceb54 + 8);
    if (result == 4) native_fn_02027410(0);
    return result;
}
u32 native_itcm_01ffa2fc(void) {
    u32 value;
    if (!native_fn_020841d0()) return 0;
    value = native_fn_020841e8();
    native_fn_02084708(native_data_021cec40, 0x20);
    native_fn_020841f4(native_fn_020125bc(), value);
    return 1;
}
u32 native_itcm_01ffa33c(void) {
    return native_fn_020846bc();
}
u32 native_itcm_01ffa440(void) {
    return native_fn_020843e4();
}
u8 *native_itcm_01ffa44c(void) {
    u8 *first = native_fn_020844d0();
    if (first[0xc0]) {
        u8 *second = native_fn_01ffa02c();
        if (*(u16 *)(first + 0x6c) == *(u16 *)second) return first + 0x50;
    }
    return 0;
}
void native_itcm_01ffa484(u32 value) {
    native_fn_02084434(1);
    native_fn_02084474(value);
}
void native_itcm_01ffa804(void) {
    native_fn_0204bb08(1);
    native_fn_02084180(1);
    native_fn_020841b8();
    native_fn_01ffa22c();
}
u32 native_itcm_01ffa824(void) {
    if (*(u32 *)(native_data_021cebe0 + 0x30) == 1) return native_fn_020ba9d0();
    return native_fn_02084568();
}
u8 native_itcm_01ffa84c(void) {
    if (*(u32 *)(native_data_021cebe0 + 0x30) != 1) return native_data_021cebe0[6];
    return 1 - native_fn_020ba9d0();
}
void native_itcm_01ffa878(void) {
    u32 value = native_fn_020846bc();
    int index;
    for (index = 1; index < 8; index++) {
        if (value & (1 << index)) native_data_021cebe0[6] = index;
    }
}
u32 native_itcm_01ffa8d8(void) {
    return native_fn_01ffa358() > 4 ? 8 : 4;
}
u32 native_itcm_01ffa948(u32 input) {
    return native_fn_01ffb4ec((u8)native_fn_01ffa8f0((s8)input))[0x166];
}
void native_itcm_01ffae5c(u32 first, u32 second, u32 third, u32 fourth, u8 fifth) {
    native_fn_01ffae9c(first, second, third, fourth);
    native_fn_02049e0c(fifth);
}
void native_itcm_01ffae70(u32 first, u32 second, u32 third, u32 fourth, u32 fifth) {
    native_fn_01ffae9c(first, second, third, fourth);
    if (fifth) native_fn_020414c8(0x3e);
    else native_fn_020414c8(0x2e);
}
void native_itcm_01ffaf98(void) {
    native_fn_02049b84(0);
    native_fn_01ffb060(0);
    native_fn_020897ec(0);
}
void native_itcm_01ffafb8(void) {
    native_fn_01ffaf98();
    native_fn_02048f7c(1);
    native_fn_0204607c();
}
void native_itcm_01ffb03c(void) {
    u8 *value = *(u8 **)(native_fn_02049ae4() + 4);
    if (value) native_data_01fff9a8[8] = *(u32 *)(value + 0x24);
}
void native_itcm_01ffb12c(u32 first, u32 second) {
    native_fn_01ffb158(first, (u16)(second + *(u32 *)native_fn_01ffb340()));
}
u8 *native_itcm_01ffb34c(void) {
    return native_fn_01ffb340() + 0x18;
}
u32 native_itcm_01ffb35c(void) {
    return native_fn_0202a634();
}
u32 native_itcm_01ffb368(void) {
    return *(u32 *)native_fn_01ffb340();
}
void native_itcm_01ffb4c4(void) {
    if (native_fn_ov000_0221794c(native_fn_01ffb340())) {
        native_fn_01ffb46c();
        native_fn_02049604(native_fn_01ffb340(), 1);
    }
}
void native_itcm_01ffb50c(u32 first, u32 second, u32 third, u32 fourth, u32 fifth) {
    native_fn_01ffb530(first, second, third, fourth, fifth, 1);
}
void native_itcm_01ffb698(u32 value) {
    native_fn_02049ffc(*(u32 *)(*native_fn_02061dcc((s8)value) + 4));
}
void native_itcm_01ffb6b8(u32 value) {
    native_fn_0205e66c(native_fn_0205e644(value));
    native_fn_0205e73c(value);
    native_fn_0205e7a8(0, value);
}
int native_itcm_01ffb734(void) {
    return *(s8 *)(native_fn_ov000_02223c54() + 0x58);
}
void native_itcm_01ffb744(void) {
    *(u32 *)native_data_01fff944 = 1;
    *(u32 *)(native_data_021cebe0 + 0x1c) = 0;
}
u32 native_itcm_01ffb768(void) {
    if (!native_fn_020b9f84(native_fn_01ffb744)) return 0;
    *(volatile u32 *)native_data_01fff944 = 0;
    return 1;
}
void native_itcm_01ffbbb4(void) {
    native_fn_ov001_021fc95c();
    native_fn_ov001_021fcf58();
    native_fn_020414b0(0x3f);
}
u32 native_itcm_01ffbfbc(u32 value) {
    if (!value) return 0;
    if (*(u32 *)(native_data_021d4100 + 0x10) == 0xf) *(u32 *)(native_data_021d4100 + 0x10) = 0x11;
    if (*(u32 *)(native_data_021d4100 + 0x10) == 0x2b) *(u32 *)(native_data_021d4100 + 0x10) = 0x2e;
    return 0x3c;
}
u32 native_itcm_01ffc184(void) {
    native_fn_01ffb8a8();
    return 1;
}
u32 native_itcm_01ffc394(void) {
    int index;
    u8 count = 0;
    index = 0;
    do {
        if (native_fn_020bb144(index)) count++;
        index++;
    } while (index < 64);
    return count;
}
void native_itcm_01fff05c(void) {
    native_fn_ov001_021fcf58();
}
