#ifndef DQM_GOAL_RESUME_LAYOUT_POSITION_H
#define DQM_GOAL_RESUME_LAYOUT_POSITION_H
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct { s16 x; s16 y; } Point;
typedef struct { u8 prefix[20]; Point position; u8 gap18[4]; void *group; u8 gap20[12]; u32 step; } LayoutState;
typedef struct { s32 selected; s32 scroll; } Selection;
typedef struct {
    u32 state;
    u8 reserved4[0x7d6];
    u8 restricted_actions : 4;
    u8 party_actions : 4;
} MenuFields;
extern MenuFields native_data_021c5a24;
extern u32 ov000_display_context_02215698(void);
extern void native_fn_0204b53c(LayoutState *, const Point *);

void native_main_02076440(const Selection *);
#endif
