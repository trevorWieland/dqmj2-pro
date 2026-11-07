#ifndef DQM_GOAL_RESUME_SELECTION_LINES_H
#define DQM_GOAL_RESUME_SELECTION_LINES_H
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct { u8 gap00[16]; s8 selector; } SelectionPanel;
extern SelectionPanel *native_fn_ov000_02217440(void);
extern u32 native_fn_ov000_022174f4(void);
extern void native_fn_ov000_02217500(u32);
extern u32 native_fn_02068de0(u32, s32, s32, s32, u8, u8, u8, u32);
extern u32 native_fn_02068f70(u32, u32, s32, u32, u8, u8, u32, u8, u8, u8, u8, u8);

void native_main_02078cbc(void);
typedef char SelectorOffset[((u32)&((SelectionPanel *)0)->selector == 16) ? 1 : -1];
#endif
