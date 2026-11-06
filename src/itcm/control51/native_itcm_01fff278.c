typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef int s32;
#define FIELD(p,t,o) (*(t *)((u8 *)(p) + (o)))
typedef struct {
    u32 low : 16;
    s32 high : 16;
} Pair;
typedef struct {
    u32 field00 : 2;
    u32 field02 : 7;
    u32 field09 : 3;
    u32 field12 : 3;
    u32 field15 : 8;
    u32 field23 : 2;
    u32 field25 : 7;
} Flags;
typedef struct {
    u32 value;
    s16 index;
    u8 text[20];
    u8 a[5];
    u8 b[5];
    Pair first;
    Pair second;
    Pair third;
    Flags flags;
} Record;
extern u32 *native_fn_020633b0(void);
extern u8 *native_fn_first_02062a10(u32);
extern u8 *native_fn_second_02062a10(u32);
extern void native_fn_02008e0c(void *, void *, u32);
extern u32 native_fn_02063e44(void *);
extern Record native_data_ov000_02246780[];

void native_itcm_01fff278(void) {
    u32 *context;
    s32 index;
    Record *out;
    u8 *source;
    s32 i;
    context = native_fn_020633b0();
    out = native_data_ov000_02246780;
    index = 0;
    do {
        if (index < 3) {
            source = native_fn_first_02062a10(FIELD((u8 *)context + index * 4, u32, 0x1c));
        } else {
            source = native_fn_second_02062a10(FIELD((u8 *)context + index * 4, u32, 0x1c));
        }
        if (!source) {
            out->index = -1;
            goto next;
        }
        native_fn_02008e0c(source, out->text, 20);
        out->index = FIELD(source, s16, 0x18);
        out->value = FIELD(source, u32, 0x14);
        out->flags.field23 = source[0x1a];
        out->flags.field00 = source[0x1b];
        out->flags.field02 = source[0x30];
        out->flags.field09 = source[0x32];
        out->flags.field15 = 0;
        out->second.low = FIELD(source, u16, 0x28);
        out->second.high = FIELD(source, s16, 0x2a);
        out->third.low = FIELD(source, u16, 0x2c);
        out->third.high = FIELD(source, s16, 0x2e);
        out->flags.field12 = (u8)native_fn_02063e44(source);
        out->first.low = FIELD(source, u16, 0x20);
        out->first.high = FIELD(source, s16, 0x22);
        out->flags.field25 = source[0x1c];
        i = 0;
        do {
            u8 *dest = (u8 *)out + i;
            u8 *pair = source + i * 2;
            dest[0x1a] = pair[0x7a];
            dest[0x1f] = pair[0x7b];
            i++;
        } while (i < 5);
    next:
        index++;
        out++;
    } while (index < 6);
}
