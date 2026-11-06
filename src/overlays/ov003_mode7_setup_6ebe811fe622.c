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

void native_ov003_021dc52c(void) {
    u8 index;
    for(index=0;index<6;index++) data_ov003_021e07f4.records[index]=0;
    switch(data_ov003_021e07e0[1]) {
    case 0:
        data_ov003_021e07f4.first=func_02062aa0();data_ov003_021e07f4.second=func_02062ad0();data_ov003_021e07f4.total=data_ov003_021e07f4.first+data_ov003_021e07f4.second;
        index=0;
        if(data_ov003_021e07f4.total) do {
            u8 *record;
            if(index<data_ov003_021e07f4.first) record=func_02062a50(index);else record=func_02062a88(index-data_ov003_021e07f4.first);
            data_ov003_021e07f4.records[index++]=record;
        } while(index<data_ov003_021e07f4.total);
        break;
    case 1:
        data_ov003_021e07f4.first=func_020c385c();data_ov003_021e07f4.second=func_020c3938();data_ov003_021e07f4.total=data_ov003_021e07f4.first+data_ov003_021e07f4.second;
        index=0;
        if(data_ov003_021e07f4.total) do {
            u8 *record;
            if(index<data_ov003_021e07f4.first) record=func_020c3838(index);else record=func_020c3914((u8)(index-data_ov003_021e07f4.first));
            data_ov003_021e07f4.records[index++]=record;
        } while(index<data_ov003_021e07f4.total);
        break;
    }
    if(data_ov003_021e07e0[1]==1) func_020625ac(1);
    func_020620b4(1);data_ov003_021e07f4.phase=1;data_ov003_021e07f4.kind=7;func_02008c58(0,data_ov003_021e07fc,240);func_02008c58(0,data_ov003_021e08ec,240);
}
