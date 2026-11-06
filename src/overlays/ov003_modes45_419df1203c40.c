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

extern Mode data_ov003_021e0a48;
extern Mode data_ov003_021e0a48_alias1;
extern Mode data_ov003_021e0a58;
extern Mode data_ov003_021e0a58_alias1;
extern char data_ov003_021e03b4[];
extern char data_ov003_021e03b8[];
extern void func_ov003_021de1b4(void);
extern void func_ov003_021de27c(void);
extern void func_ov003_021de4b8(void);
extern void func_ov003_021de5b0(void);
extern void func_ov003_021df668(u32);
extern void func_ov003_021dccc4(u32);
extern u32 func_020c3a00(void);

u32 native_ov003_021de064(void) {Input *input=func_0202a634();if(input->pressed&0xFF7){func_ov003_021df668(1);func_ov003_021dfd18(1);return 1;}return 0;}

void native_ov003_021de09c(void) {func_02048e74(&data_ov003_021e0a48,4);func_02048fcc(func_ov003_021dad9c());if(func_ov003_021dada8()==7)*func_ov003_021dad9c()=1;else *func_ov003_021dad9c()=0;data_ov003_021e0a48_alias1.phase=0;}

u32 native_ov003_021de0f0(void) {
    Mode *mode=&data_ov003_021e0a48_alias1;u32 result=data_ov003_021e0a48.result;
    switch(data_ov003_021e0a48.phase){case 0:func_ov003_021de1b4();func_ov003_021dff60(func_ov003_021dad9c());func_ov003_021df6ac(func_ov003_021dad9c());mode->phase=1;break;case 1:func_ov003_021de27c();func_ov003_021dff60(func_ov003_021dad9c());func_ov003_021df6ac(func_ov003_021dad9c());break;case 3:result=5;break;case 4:result=7;break;case 2:result=0;break;}return result;
}

void native_ov003_021de180(void) {if(data_ov003_021e0a48.phase==3)func_ov003_021df4b4(2);else func_ov003_021df4b4(1);func_ov003_021dfccc();}

void native_ov003_021de1b4(void) {
    s32 *cursor;if(func_ov003_021dada8()!=5)func_ov003_021ded08(func_ov003_021dad9c(),3,16,1,3,30,2,0);cursor=func_ov003_021dad9c();func_ov003_021deda4(cursor,2,data_ov003_021e03b4,2,6,28,*func_ov003_021dad9c());func_ov003_021dfd18(1);if(func_ov003_021dada8()!=5)func_020620e8(35,1);if(func_02041944())func_02041538(0,2,10);
}

void native_ov003_021de27c(void) {
    Input *input=func_0202a634();s32 *cursor=func_ov003_021dad9c();
    if(input->repeat&64){if(*cursor>0)*cursor=*cursor-1;else *cursor=1;func_0205e7a8(-1,85);}else if(input->repeat&128){if(*cursor<1)*cursor=*cursor+1;else *cursor=0;func_0205e7a8(-1,85);}
    if(input->repeat&1){switch(*cursor){case 0:data_ov003_021e0a48.phase=3;break;case 1:func_02041538(1,2,10);func_ov003_021dccc4(0);data_ov003_021e0a48.phase=4;break;}func_0205e7a8(-1,82);return;}if(input->repeat&2){data_ov003_021e0a48.phase=2;func_0205e7a8(-1,83);}
}

void native_ov003_021de378(void) {func_02048e74(&data_ov003_021e0a58,5);func_02048fcc(func_ov003_021dad9c());if(func_020c3a00()==4)*func_ov003_021dad9c()=1;else *func_ov003_021dad9c()=0;func_020c39f0(1);data_ov003_021e0a58_alias1.phase=0;}

u32 native_ov003_021de3d4(void) {
    Mode *mode=&data_ov003_021e0a58_alias1;u32 result=data_ov003_021e0a58.result;
    switch(data_ov003_021e0a58.phase){case 0:func_ov003_021de4b8();func_ov003_021dff60(func_ov003_021dad9c());func_ov003_021df6ac(func_ov003_021dad9c());mode->phase=2;break;case 2:func_ov003_021dff60(func_ov003_021dad9c());if(func_02041814()!=1)mode->phase=1;break;case 1:func_ov003_021de5b0();func_ov003_021dff60(func_ov003_021dad9c());func_ov003_021df6ac(func_ov003_021dad9c());break;case 4:result=10;break;case 5:result=11;break;case 3:result=4;break;}return result;
}

void native_ov003_021de484(void) {if(data_ov003_021e0a58.phase==3)func_ov003_021df4b4(2);else func_ov003_021df4b4(1);func_ov003_021dfccc();}

void native_ov003_021de4b8(void) {
    s32 *cursor;if(func_ov003_021dada8()!=4)func_ov003_021ded08(func_ov003_021dad9c(),3,16,1,3,30,2,0);func_ov003_021ded08(func_ov003_021dad9c(),23,16,2,5,29,2,1);cursor=func_ov003_021dad9c();func_ov003_021deda4(cursor,2,data_ov003_021e03b8,2,8,28,*func_ov003_021dad9c());func_ov003_021dfd18(1);if(func_ov003_021dada8()!=4)func_020620e8(35,1);if(func_02041944())func_02041538(0,2,10);
}

void native_ov003_021de5b0(void) {
    Input *input=func_0202a634();s32 *cursor=func_ov003_021dad9c();
    if(input->repeat&64){if(*cursor>0)*cursor=*cursor-1;else *cursor=1;func_0205e7a8(-1,85);}else if(input->repeat&128){if(*cursor<1)*cursor=*cursor+1;else *cursor=0;func_0205e7a8(-1,85);}
    if(input->repeat&1){switch(*cursor){case 0:data_ov003_021e0a58.phase=4;break;case 1:func_020c39f0(4);data_ov003_021e0a58.phase=5;break;}func_02041538(1,2,10);func_02061260(1);func_0205e7a8(-1,82);return;}if(input->repeat&2){data_ov003_021e0a58.phase=3;func_0205e7a8(-1,83);}
}
