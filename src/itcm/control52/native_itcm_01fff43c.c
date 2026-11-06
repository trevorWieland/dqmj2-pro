typedef signed char s8;
typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef int s32;
#define FIELD(p,t,o) (*(t *)((u8 *)(p) + (o)))
typedef struct {
    u32 low : 16;
    u32 high : 16;
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
typedef struct {
    s16 x;
    s16 y;
} Point;
typedef struct {
    u8 a;
    u8 b;
} Entry;
typedef struct {
    Point point;
    u8 reserved[28];
    Entry entries[5];
} Frame;
extern void native_fn_02008e0c(void *, void *, u32);
extern void native_fn_0207b460(s16, u8, Entry *, u8 *);
extern void native_fn_0207b1c4(Entry *, u8 *, u8 *);
extern void native_fn_0207c078(s16, u8, u8 *, u8 *);
extern u32 native_fn_0207c2b8(Point *, u8 *);
extern u32 native_fn_0207c3d8(Point *, u8 *);

static inline void zip_one(Record *input, u8 *output, Entry *entries, s32 index) {
    u8 *from = (u8 *)input + index;
    Entry *entry = &entries[index];
    u8 *dest = output + index * 2;
    entries[index].a = from[0x1a];
    entry->b = from[0x1f];
    dest[0xd6] = from[0x1a];
}

void native_itcm_01fff43c(Record *source, u8 *output, s32 arg2, s32 arg3) {
    Frame frame;
    s32 index;
    if (source == 0 || source->index == -1) {
        FIELD(output, s32, 0) = -1;
        FIELD(output, s16, 0x2e) = -1;
        FIELD(output, s32, 4) = -1;
        return;
    }
    native_fn_02008e0c(source->text, output + 0xb6, 20);
    index = 0;
    FIELD(output, s32, 0) = source->index;
    FIELD(output, s16, 0x2e) = source->index;
    FIELD(output, u32, 4) = source->value;
    FIELD(output, u8, 0x30) = source->flags.field23;
    FIELD(output, u16, 0x11c) = source->first.low;
    FIELD(output, s16, 0x11e) = source->first.high;
    FIELD(output, u16, 0x124) = source->second.low;
    FIELD(output, s16, 0x126) = source->second.high;
    FIELD(output, u16, 0x128) = source->third.low;
    FIELD(output, s16, 0x12a) = source->third.high;
    FIELD(output, s8, 0x12c) = source->flags.field02;
    FIELD(output, s8, 0x12e) = source->flags.field09;
    FIELD(output, s8, 0x12d) = source->flags.field15;
    FIELD(output, s32, 0x130) = arg2;
    FIELD(output, s32, 0x134) = arg3;
    FIELD(output, s8, 0xaf) = source->flags.field25;
    FIELD(output, s8, 0xac) = source->flags.field12;
    do {
        zip_one(source, output, frame.entries, index);
        index++;
    } while (index < 5);
    native_fn_0207b460(FIELD(output, s16, 0x2e), FIELD(output, u8, 0x30), frame.entries, output + 0x4a);
    native_fn_0207b1c4(frame.entries, output + 0x4a, output + 0xc);
    native_fn_0207c078(FIELD(output, s16, 0x2e), FIELD(output, u8, 0x30), output + 0x4a, output + 0x8a);
    frame.point.x = FIELD(output, s16, 0x11c);
    frame.point.y = FIELD(output, s16, 0x11e);
    FIELD(output, s16, 0x120) = native_fn_0207c2b8(&frame.point, output + 0x4a);
    FIELD(output, s16, 0x122) = native_fn_0207c3d8(&frame.point, output + 0x4a);
}
