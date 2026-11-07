#ifndef DQM_GOAL_RESUME_LAYOUT_SETUP_H
#define DQM_GOAL_RESUME_LAYOUT_SETUP_H
typedef unsigned char u8;
typedef unsigned int u32;
typedef signed short s16;
typedef struct { s16 x; s16 y; } Point;
typedef struct {
    u32 field0;
    u8 reserved04[16];
    Point position;
    u8 gap18[4];
    void *group;
    u8 field20;
    u8 field21;
    u8 object_count;
    u8 gap23[9];
    u32 step;
    u32 field30;
    u32 bank;
    u8 reserved38[16];
} LayoutState;
typedef struct { u8 prefix[16]; LayoutState layout; } Display;
extern Display *native_fn_ov000_02215698(void);
extern void native_fn_ov000_022159b8(const char *, u32);
extern void native_fn_0204b4f4(LayoutState *, const Point *, u32, u32, u32, u8);
extern void native_fn_0204b61c(LayoutState *, u32);
extern const char native_data_020de3f8[];
void native_main_020763cc(void);
typedef char PointSize[(sizeof(Point) == 4) ? 1 : -1];
typedef char LayoutSize[(sizeof(LayoutState) == 72) ? 1 : -1];
typedef char LayoutOffset[((u32)&((Display *)0)->layout == 16) ? 1 : -1];
#endif
