typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {u16 pad,pressed,unused,repeated;} Input;
extern u32 data_ov003_021e07bc[];
extern u32 data_ov003_021e07bc_alias1[];
extern u32 data_ov003_021e07cc[];
extern u32 data_ov003_021e07d0[];
extern char data_ov003_021e034c[];
extern u32 *func_ov003_021dad9c(void);
extern u32 func_ov003_021dada8(void);
extern void func_02048e74(void *,u32);
extern void func_02048fcc(void *);
extern void func_ov003_021dbb18(void);
extern u32 func_02041944(void);
extern void func_02041538(u32,u32,u32);
extern void func_ov003_021dff60(void *);
extern void func_ov003_021df6ac(void *);
extern void func_ov003_021dbbc4(void);
extern void func_ov003_021dccc4(u32);
extern void func_ov003_021df4b4(u32);
extern void func_ov003_021dfccc(void);
extern void func_ov003_021ded08(void *,u32,u32,u32,u32,u32,u32,u32);
extern void func_ov003_021deda4(void *,u32,void *,u32,u32,u32,u32);
extern void func_ov003_021dfd18(u32);
extern void func_020620e8(u32,u32);
extern Input *func_0202a634(void);
extern void func_0205e7a8(s32,u32);
extern u32 func_0202a1e0(u32);
extern void func_ov003_021df518(void);
extern void func_02068ae8(void);
extern void func_0207ca14(u32);
extern void func_020bf518(u32);
extern void func_0206258c(u32);
extern void func_ov003_021dbe4c(void);
extern u32 func_ov003_021dc060(void);
extern void func_ov003_021dbf68(void);
extern void func_ov003_021dc1e8(void);
extern u32 func_020c4318(void);
extern void func_02068f60(void);
extern void func_020625ac(u32);
extern void func_020693e0(void);
extern void func_02068d54(void);
extern void func_020c0210(void);
extern void func_020c013c(void);
extern void func_0207cdb8(u32);
extern void func_020bf5c0(u32);
extern void func_ov003_021deb78(void *,u32);
extern u32 func_02048f8c(u32);
extern void func_ov003_021dad1c(u32,u32);

void native_ov003_021db9bc(void) {
    func_02048e74(data_ov003_021e07bc_alias1,1);func_02048fcc(func_ov003_021dad9c());
    switch(func_ov003_021dada8()) {
    case 2:*func_ov003_021dad9c()=0;break;
    case 7:*func_ov003_021dad9c()=1;break;
    }
    data_ov003_021e07bc[1]=0;
}

u32 native_ov003_021dba20(void) {
    u32 *pending;
    u32 result;
    result=data_ov003_021e07bc[0];pending=data_ov003_021e07bc_alias1;
    switch(data_ov003_021e07bc[1]) {
    case 0:func_ov003_021dbb18();if(func_02041944()) func_02041538(0,2,10);func_ov003_021dff60(func_ov003_021dad9c());func_ov003_021df6ac(func_ov003_021dad9c());pending[1]=1;break;
    case 1:func_ov003_021dbbc4();func_ov003_021dff60(func_ov003_021dad9c());func_ov003_021df6ac(func_ov003_021dad9c());break;
    case 2:result=2;break;
    case 3:func_02041538(1,2,10);func_ov003_021dccc4(1);result=7;break;
    case 4:result=0;break;
    }
    return result;
}

void native_ov003_021dbae4(void) {
    if(data_ov003_021e07bc[1]==2) func_ov003_021df4b4(2);else func_ov003_021df4b4(1);func_ov003_021dfccc();
}

void native_ov003_021dbb18(void) {
    u32 *context;
    u32 *selected;
    if(func_ov003_021dada8()!=2) func_ov003_021ded08(func_ov003_021dad9c(),2,16,1,3,30,2,0);
    context=func_ov003_021dad9c();selected=func_ov003_021dad9c();
    func_ov003_021deda4(context,2,data_ov003_021e034c,2,6,28,*selected);func_ov003_021dfd18(1);
    if(func_ov003_021dada8()!=2) func_020620e8(37,1);
}

void native_ov003_021dbbc4(void) {
    Input *input=func_0202a634();s32 *context=(s32 *)func_ov003_021dad9c();
    if(input->repeated&64) {if(*context>0) *context=*context-1;else *context=1;func_0205e7a8(-1,85);}
    else if(input->repeated&128) {if(*context<1) *context=*context+1;else *context=0;func_0205e7a8(-1,85);}
    if(input->pressed&1) {
        switch(*context) {case 0:data_ov003_021e07bc[1]=2;break;case 1:data_ov003_021e07bc[1]=3;break;}
        func_0205e7a8(-1,82);
    } else if(input->pressed&2) {data_ov003_021e07bc[1]=4;func_0205e7a8(-1,83);}
}

void native_ov003_021dbca0(void) {
    u32 heap;
    func_02048e74(data_ov003_021e07d0,3);func_02048fcc(func_ov003_021dad9c());heap=func_0202a1e0(1);func_ov003_021df518();func_02068ae8();func_0207ca14(1);func_020bf518(1);func_0202a1e0(heap);
    data_ov003_021e07cc[0]=1;data_ov003_021e07cc[2]=0;((u8 *)func_ov003_021dad9c())[16]=3;func_0206258c(0);
}

void native_ov003_021dbdec(void) {
    func_0206258c(1);func_020625ac(0);func_020693e0();func_02068d54();func_020c0210();func_020c013c();func_0207cdb8(1);func_020bf5c0(1);func_ov003_021df518();func_ov003_021dfccc();func_ov003_021deb78(func_ov003_021dad9c(),0);func_ov003_021dad1c(2,func_02048f8c(1));
}
