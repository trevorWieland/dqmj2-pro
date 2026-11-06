typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {u32 result,phase;} Mode;
typedef struct {u16 unused,pressed,pad,repeat;} Input;
extern Mode data_ov003_021e0a08;
extern Mode data_ov003_021e0a08_alias1;
extern char data_ov003_021e0350[];
extern void func_02048e74(void *,u32);
extern s32 *func_ov003_021dad9c(void);
extern u32 func_ov003_021dada8(void);
extern void func_02048fcc(void *);
extern void func_ov003_021dce68(void);
extern void func_ov003_021dcf60(void);
extern void func_ov003_021dff60(void *);
extern void func_ov003_021df6ac(void *);
extern u32 func_02041814(void);
extern void func_ov003_021df4b4(u32);
extern void func_ov003_021dfccc(void);
extern void func_ov003_021ded08(void *,u32,u32,u32,u32,u32,u32,u32);
extern void func_ov003_021deda4(void *,u32,void *,u32,u32,u32,u32);
extern void func_ov003_021dfd18(u32);
extern void func_020620e8(u32,u32);
extern u32 func_02041944(void);
extern void func_02041538(u32,u32,u32);
extern Input *func_0202a634(void);
extern void func_0205e7a8(s32,u32);
extern void func_020c356c(u32);
extern void func_020c39f0(u32);
extern void func_02061260(u32);

void native_ov003_021dcd3c(void) {
    func_02048e74(&data_ov003_021e0a08,2);func_02048fcc(func_ov003_021dad9c());
    if(func_ov003_021dada8()==12) *func_ov003_021dad9c()=1;
    data_ov003_021e0a08_alias1.phase=0;
}

u32 native_ov003_021dcd84(void) {
    Mode *mode=&data_ov003_021e0a08_alias1;
    u32 result=data_ov003_021e0a08.result;
    switch(data_ov003_021e0a08.phase) {
    case 0:func_ov003_021dce68();func_ov003_021dff60(func_ov003_021dad9c());func_ov003_021df6ac(func_ov003_021dad9c());mode->phase=1;break;
    case 1:func_ov003_021dff60(func_ov003_021dad9c());if(func_02041814()!=1)mode->phase=2;break;
    case 2:func_ov003_021dcf60();func_ov003_021dff60(func_ov003_021dad9c());func_ov003_021df6ac(func_ov003_021dad9c());break;
    case 3:result=3;break;
    case 4:result=11;break;
    case 5:result=1;break;
    }
    return result;
}

void native_ov003_021dce34(void) {
    if(data_ov003_021e0a08.phase==5)func_ov003_021df4b4(2);else func_ov003_021df4b4(1);
    func_ov003_021dfccc();
}

void native_ov003_021dcf60(void) {
    Input *input=func_0202a634();s32 *cursor=func_ov003_021dad9c();
    if(input->repeat&64){if(*cursor>0)*cursor=*cursor-1;else *cursor=1;func_0205e7a8(-1,85);}
    else if(input->repeat&128){if(*cursor<1)*cursor=*cursor+1;else *cursor=0;func_0205e7a8(-1,85);}
    if(input->pressed&1){switch(*cursor){case 0:func_020c356c(0);data_ov003_021e0a08.phase=3;break;case 1:func_020c356c(1);func_020c39f0(3);data_ov003_021e0a08.phase=4;break;}func_02041538(1,2,10);func_02061260(1);func_0205e7a8(-1,82);}
    else if(input->pressed&2){data_ov003_021e0a08.phase=5;func_0205e7a8(-1,83);}
}
