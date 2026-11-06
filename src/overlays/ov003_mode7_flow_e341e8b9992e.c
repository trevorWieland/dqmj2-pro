typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {u16 pad,pressed,unused,repeated;} Input;
typedef struct {u32 index;u8 pad[8];u16 count;} Selection;
typedef struct {u32 phase,kind;u8 pad[240];u32 chosen;u8 reserved[236];u8 *record;u8 last[8];u8 *records[8];} Display;
extern u8 data_ov003_021e07e0[];
extern u32 data_ov003_021e07e4[];
extern Selection data_ov003_021e07fc;
extern Selection data_ov003_021e08ec;
extern Display data_ov003_021e07f4;
extern Input *func_0202a634(void);
extern void func_02049f24(void);
extern void func_ov003_021dc52c(void);
extern void *func_ov003_021dad9c(void);
extern void func_ov003_021debd8(void *,u32,u32,u32);
extern void func_ov003_021df4b4(u32);
extern void func_ov003_021dc6c0(u32);
extern void func_0206dcd0(void *);
extern u32 func_02041944(void);
extern void func_02041538(u32,u32,u32);
extern u32 func_020491f8(Selection *);
extern void func_ov003_021dccd4(Selection *);
extern void func_0205e7a8(int,u32);
extern void func_ov003_021dcbc4(void);
extern void func_ov003_021dcc8c(void);
extern void func_02048e74(void *,u32);
extern void func_02048fcc(void *);
extern void func_ov003_021df518(void);
extern void func_0206258c(u32);
extern void func_020625ac(u32);
extern void func_ov003_021dfccc(void);
extern void func_ov003_021deb78(void *,u32);

void native_ov003_021dc214(void) {
    func_02048e74(data_ov003_021e07e4,7);func_02048fcc(func_ov003_021dad9c());func_ov003_021df518();func_0206258c(0);data_ov003_021e07f4.phase=0;data_ov003_021e07f4.kind=7;
}

u32 native_ov003_021dc258(void) {
    Display *display;
    Selection *primary;
    volatile Selection *active=0;
    u32 again;
    u32 result;
    Input *input=func_0202a634();
    u32 render=1;
    func_02049f24();
    result=*(u32 *)(data_ov003_021e07e0+4);
    primary=&data_ov003_021e07fc;
    display=&data_ov003_021e07f4;
    do {
        again=0;
        switch(display->phase) {
        case 0:func_ov003_021dc52c();func_ov003_021debd8(func_ov003_021dad9c(),5,0,5);render=0;break;
        case 1:
            active=primary;func_ov003_021df4b4(1);func_ov003_021dc6c0(2);func_0206dcd0(display->records[primary->index]);if(func_02041944()) func_02041538(0,2,10);display->phase=2;again=1;break;
        case 2:
            active=primary;
            if(func_020491f8(primary)) {func_0206dcd0(display->records[primary->index]);func_ov003_021dccd4(primary);func_0205e7a8(-1,85);}
            if(input->pressed&1) {
                u32 selected=active->index;
                if(selected!=active->count-1) {display->phase=3;display->record=display->records[selected];func_0205e7a8(-1,82);}
                else {
                    switch(data_ov003_021e07e0[1]) {case 0:result=4;break;case 1:result=1;break;}
                    func_02041538(1,2,10);func_0205e7a8(-1,83);
                }
            } else if(input->pressed&2) {
                switch(data_ov003_021e07e0[1]) {case 0:result=4;break;case 1:result=1;break;}
                func_0205e7a8(-1,83);func_02041538(1,2,10);
            }
            break;
        case 3:active=&data_ov003_021e08ec;func_ov003_021df4b4(1);func_ov003_021dc6c0(4);display->phase=4;again=1;break;
        case 4:
            active=&data_ov003_021e08ec;
            if(func_020491f8(active)) func_0205e7a8(-1,85);
            if(input->pressed&1) {display->record[50]=(u8)display->chosen;display->phase=1;func_0205e7a8(-1,82);}
            else if(input->pressed&2) {display->phase=1;func_0205e7a8(-1,83);}
            else if(input->pressed&0x800) func_ov003_021dcbc4();
            break;
        case 5:active=&data_ov003_021e08ec;func_ov003_021dcc8c();break;
        }
        if(render) func_ov003_021dccd4(active);
    } while(again);
    return result;
}

void native_ov003_021dc500(void) {
    func_020625ac(0);func_0206258c(1);func_ov003_021df518();func_ov003_021dfccc();func_ov003_021deb78(func_ov003_021dad9c(),0);
}
