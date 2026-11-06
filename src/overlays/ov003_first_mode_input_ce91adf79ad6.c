typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {u16 pad,pressed,unused,repeated;} Input;
typedef struct {u8 choice;u8 pad[3];u32 current;u32 phase;} State;
extern State data_ov003_021e07a8;
extern Input *func_0202a634(void);
extern s32 *func_ov003_021dad9c(void);
extern void func_0205e7a8(s32,u32);
extern u32 func_020c367c(void);
extern u32 func_ov003_021db57c(u32);
extern void func_ov003_021db20c(u32,u32);
extern void func_ov003_021db290(void);
extern void func_ov003_021dea38(u32,u32,u32,u32,u32,s32);
extern void func_ov003_021dfd18(u32);
extern void func_ov003_021df668(u32);

void native_ov003_021db034(void) {
    Input *input=func_0202a634();
    s32 *context=func_ov003_021dad9c();
    if(input->repeated&64) {if(*context>0) *context=*context-1;else *context=4;func_0205e7a8(-1,85);}
    else if(input->repeated&128) {if(*context<4) *context=*context+1;else *context=0;func_0205e7a8(-1,85);}
    if(input->pressed&1) {
        u32 success=0;
        u32 mode=0;
        switch(*context) {
        case 0:
            switch(func_020c367c()) {
            case 1:success=func_ov003_021db57c(1);mode=2;break;
            case 2:success=func_ov003_021db57c(0);mode=1;break;
            }
            if(success) {func_ov003_021db20c(mode,0);data_ov003_021e07a8.choice=1;data_ov003_021e07a8.phase=6;func_0205e7a8(-1,83);}
            else {func_ov003_021db290();func_ov003_021db20c(0,1);data_ov003_021e07a8.choice=2;data_ov003_021e07a8.phase=6;}
            break;
        case 1:data_ov003_021e07a8.phase=3;func_0205e7a8(-1,82);break;
        case 2:data_ov003_021e07a8.phase=4;func_0205e7a8(-1,82);break;
        case 3:data_ov003_021e07a8.phase=5;func_0205e7a8(-1,82);break;
        case 4:data_ov003_021e07a8.phase=7;func_0205e7a8(-1,83);break;
        }
    } else if(input->pressed&2) {data_ov003_021e07a8.phase=7;func_0205e7a8(-1,83);}
}

void native_ov003_021db20c(u32 message,u32 failure) {
    s32 response=-1;
    if(failure) response=87;
    func_ov003_021dea38(20,1,message,1,1,response);func_ov003_021dfd18(0);
}

void native_ov003_021db248(void) {
    Input *input=func_0202a634();
    if(input->pressed&0xFF7) {
        if(data_ov003_021e07a8.choice!=2) func_ov003_021df668(1);
        data_ov003_021e07a8.phase=data_ov003_021e07a8.choice;
    }
}
