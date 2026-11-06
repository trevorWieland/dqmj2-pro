typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef int s32;
typedef struct {u32 first,second;} SavedCursor;
typedef struct {u32 phase,kind;u8 pad[240];u32 chosen;u8 reserved[236];u8 *record;u8 total,first,second,unknown;u32 unused;u8 *records[6];} Display;
extern Display data_ov003_021e07f4;
extern u8 data_ov003_021e07e0[];
extern u8 data_ov003_021e07fc[];
extern u8 data_ov003_021e08ec[];
extern u32 func_02062aa0(void);
extern u32 func_02062ad0(void);
extern u8 *func_02062a50(u32);
extern u8 *func_02062a88(u32);
extern u32 func_020c385c(void);
extern u32 func_020c3938(void);
extern u8 *func_020c3838(u32);
extern u8 *func_020c3914(u32);
extern void func_020625ac(u32);
extern void func_020620b4(u32);
extern void func_02008c58(u32,void *,u32);
extern u8 *func_ov003_021dad9c(void);
extern void func_ov003_021deb60(u32,u32,u32);
extern void func_ov003_021deedc(void *,u32,u32,u32,u32,u32,u32,u32,u32);
extern void func_ov003_021dfd18(u32);
extern void func_ov003_021dfd50(u32,u32,u32);
extern void func_ov003_021dec40(void *,u32);
extern void func_ov003_021de868(u32,s32,u32,u32,u32,u32,u32,u32,u32);
extern void func_ov003_021deda4(void *,u32,void *,u32,u32,u32,u32);
extern void func_ov003_021dc820(u32);

void native_ov003_021dc6c0(u32 kind) {
    u32 *cursor;
    u8 *context=func_ov003_021dad9c();
    switch(kind) {
    case 2: {
        u8 rows=(u8)(data_ov003_021e07f4.total+1);
        u32 first,second;
        cursor=(u32 *)data_ov003_021e07fc;
        data_ov003_021e07e0[0]=data_ov003_021e07f4.total;
        first=cursor[0];second=cursor[1];
        func_ov003_021deb60(5,0,5);func_ov003_021deedc(cursor,1,3,28,rows,rows,1,15,1);cursor[0]=first;cursor[1]=second;func_ov003_021dfd18(1);func_ov003_021dfd50(224,64,1);
        break;
    }
    case 4:
        cursor=(u32 *)data_ov003_021e08ec;
        func_ov003_021dec40(func_ov003_021dad9c(),1);func_ov003_021de868(5,(s8)context[16],2,1,3,30,2,0,1);data_ov003_021e07e0[0]=5;func_ov003_021deda4(cursor,5,0,2,6,28,0);cursor[0]=data_ov003_021e07f4.record[50];func_ov003_021dfd18(1);func_ov003_021dfd50(224,0,0);break;
    }
    func_ov003_021dc820(kind);
}
