#ifndef DQM_GOAL_RESUME_CHOICE_PROMPT_H
#define DQM_GOAL_RESUME_CHOICE_PROMPT_H
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct TextBinding TextBinding;
typedef struct { const u16 *stream; TextBinding *binding; } TextBindingSlot;
typedef struct TextFont TextFont;
extern TextBindingSlot *native_fn_02049ae4(void);
extern u16 *native_fn_02049f24(void);
extern void native_fn_02049f30(void);
extern u32 native_fn_0206c100(void);
extern s32 native_fn_0206c120(void);
extern const u8 *native_fn_0205dc70(s32, s32, s32);
extern void native_fn_02046af4(TextFont *, const u8 *, u32, u32, u16 *, u32);
extern void native_fn_02049f14(u16 *);
extern void native_fn_ov000_02217bdc(u32, u32, u32, u32, u32, u32);
extern void native_fn_020853c8(TextBinding *, const u16 *);
extern void native_fn_02068f60(u32);
extern void native_fn_0206b35c(void);
extern TextFont native_data_021c9698;

u32 native_main_02078b30(void);
typedef char TextSlotSize[(sizeof(TextBindingSlot) == 8) ? 1 : -1];
#endif
