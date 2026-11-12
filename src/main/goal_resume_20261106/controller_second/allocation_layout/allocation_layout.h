#ifndef DQM_GOAL_RESUME_ALLOCATION_LAYOUT_H
#define DQM_GOAL_RESUME_ALLOCATION_LAYOUT_H
typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef signed short s16;
typedef struct { s16 x; s16 y; } Point;
typedef struct { s32 selected; s32 scroll; } Selection;
typedef struct LayoutState LayoutState;
extern void *ov000_display_context_02215698(void);
extern void native_fn_0204b53c(LayoutState *, const Point *);
extern u32 native_data_021c6234;
void native_main_02078818(const Selection *);
typedef char PointSize[(sizeof(Point) == 4) ? 1 : -1];
typedef char SelectionSize[(sizeof(Selection) == 8) ? 1 : -1];
#endif
