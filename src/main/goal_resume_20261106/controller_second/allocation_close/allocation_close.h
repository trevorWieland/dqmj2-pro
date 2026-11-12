#ifndef DQM_GOAL_RESUME_ALLOCATION_CLOSE_H
#define DQM_GOAL_RESUME_ALLOCATION_CLOSE_H
typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef signed char s8;
typedef unsigned short u16;
typedef struct { s32 selected; s32 scroll; u32 field08; u16 displayed_count; u8 gap0e[2]; } SelectionList;
typedef struct { u32 state; u8 gap04[0xf8]; SelectionList skill_selection; u8 gap10c[0x1c7]; u8 close_mode; } AllocationMenu;
typedef struct LayoutState LayoutState;
typedef struct TextOwner TextOwner;
extern AllocationMenu native_data_021c6234;
extern void *ov000_display_context_02215698(void);
extern void native_fn_0204b61c(LayoutState *, int);
extern u32 native_fn_020620e8(s8, u32);
extern TextOwner *native_fn_02049ad0(s32);
extern u32 native_fn_ov000_022162c0(TextOwner *);
extern void native_fn_ov000_02216664(SelectionList *);
extern void native_fn_ov000_021e7b9c(u32);
extern void native_fn_ov000_0221570c(u32);

void native_main_020771d4(u32);
typedef char ListSize[(sizeof(SelectionList) == 16) ? 1 : -1];
typedef char ListCount[((u32)&((SelectionList *)0)->displayed_count == 12) ? 1 : -1];
typedef char ListOffset[((u32)&((AllocationMenu *)0)->skill_selection == 0xfc) ? 1 : -1];
typedef char CloseModeOffset[((u32)&((AllocationMenu *)0)->close_mode == 0x2d3) ? 1 : -1];
#endif
