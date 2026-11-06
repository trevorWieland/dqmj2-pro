typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {u16 pad,pressed,unused,repeated;} Input;
extern u32 data_ov003_021e07cc[];
extern u32 data_ov003_021e07cc_alias1[];
extern void *func_ov003_021dad9c(void);
extern void func_ov003_021deb78(void *,u32);
extern void func_ov003_021dec40(void *,u32);
extern void func_ov003_021df190(void *);
extern void func_ov003_021dfe30(void);
extern void func_020c17e8(u32,u32);
extern u32 func_020c1708(void *);
extern u32 func_02048f8c(u32);
extern void func_ov003_021dad1c(u32,u32);
extern void func_ov003_021dfda8(u32);
extern void func_020625ac(u32);
extern void func_020620b4(u32);
extern u32 func_020c3828(u32);
extern void *func_02062a10(u32);
extern void func_0206dcd0(void *);
extern void func_02062358(u32);
extern void func_020c48bc(void);
extern void func_020c48d0(u32,u32,u32);
extern u32 func_02048f7c(u32);
extern void func_020c484c(u32);
extern void func_020c48e8(u32);
extern Input *func_0202a634(void);
extern void func_0206940c(void);
extern u32 func_020698f4(u32);
extern void func_ov003_021dc138(void);
extern void func_ov003_021dc1c0(void);
extern void func_0205e7a8(s32,u32);
extern u32 func_0206a04c(void);
extern void func_ov003_021df150(u32,s32);
extern void func_020c485c(void);
extern void func_02068f60(u32);
extern void func_0206a06c(u32);
extern void func_ov003_021dbed8(u32);
extern u32 func_0206be2c(void);
extern u32 func_020c1540(void);
extern u32 func_0206a0fc(u32);
extern u32 func_0206a49c(void);
extern u32 func_0206c0b0(void);
extern u32 func_0206c0e0(void);
extern u32 func_020c17b0(void);
extern void func_02008d78(void *,u32,u32);
extern void func_020c3790(void *);
extern void func_020c386c(void *);
extern void func_0206bc80(void *,u8 *);
extern void func_020c384c(u8);
extern void func_0206bd24(void *,u8 *);
extern void func_020c3928(u8);
extern void func_02041538(u32,u32,u32);
extern u32 func_0206bf34(void);

void native_ov003_021dbe4c(void) {
    s32 selected;
    func_ov003_021deb78(func_ov003_021dad9c(),14);func_ov003_021dec40(func_ov003_021dad9c(),0);func_ov003_021df190(func_ov003_021dad9c());func_ov003_021dfe30();func_020c17e8(0,0);selected=-1;func_020c1708(&selected);
    func_ov003_021dad1c(12,func_02048f8c(1));func_ov003_021dfda8(1);func_020625ac(1);func_020620b4(1);func_0206dcd0(func_02062a10(func_020c3828(0)));func_02062358(1);
}

void native_ov003_021dbed8(u32 option) {
    func_020c48bc();
    switch(option) {
    case 0:break;
    case 1:func_020c48d0(5,6,27);break;
    case 2:func_020c48d0(5,6,28);break;
    case 3:func_020c48d0(5,6,29);break;
    case 4:func_020c48d0(5,6,48);break;
    }
    func_020c484c(func_02048f7c(1));func_020c48e8(87);
}

void native_ov003_021dbf68(void) {
    Input *input=func_0202a634();
    func_0206940c();
    if(input->pressed&1) {
        switch(func_020698f4(0)) {
        case 1:func_ov003_021dc138();func_0205e7a8(-1,82);break;
        case 2:func_ov003_021dc1c0();func_0205e7a8(-1,83);break;
        default:
            if(func_0206a04c()==2) {func_ov003_021df150(3,-1);func_020c485c();func_02068f60(0);data_ov003_021e07cc[2]=2;}
            break;
        }
    } else if(input->pressed&2) func_0206a06c(1);
    if(input->pressed&4) {
        if(!func_020c1708(data_ov003_021e07cc_alias1)) return;
        func_ov003_021dbed8(data_ov003_021e07cc[0]);func_0206dcd0(func_02062a10(func_0206be2c()));func_02068f60(0);data_ov003_021e07cc[2]=2;
    }
}

u32 native_ov003_021dc060(void) {
    u8 busy;
    u32 result=0;
    busy=func_020c1540();
    if(!busy) {
        switch(func_0206a0fc(0)-1) {
        case 0:func_ov003_021dc138();func_0205e7a8(-1,82);break;
        case 1:func_ov003_021dc1c0();func_0205e7a8(-1,83);break;
        default: {
            u32 status=func_0206a49c();
            if(status==1) {func_ov003_021df150(3,-1);func_020c485c();func_02068f60(0);data_ov003_021e07cc[2]=2;}
            else if(status==2) func_0205e7a8(-1,84);
            break;
        }
        }
    }
    if(func_0206c0b0() || func_0206c0e0() || func_020c17b0() || busy) result=1;
    return result;
}

void native_ov003_021dc138(void) {
    u32 ids[3];
    u8 selected;
    func_02008d78(ids,0,12);func_020c3790(ids);func_020c386c(ids);func_0206bc80(ids,&selected);func_020c3790(ids);func_020c384c(selected);func_0206bd24(ids,&selected);func_020c3928(selected);func_020c386c(ids);func_02041538(1,2,10);data_ov003_021e07cc[2]=3;
}

void native_ov003_021dc1c0(void) {func_02041538(1,2,10);data_ov003_021e07cc[2]=4;}

void native_ov003_021dc1e8(void) {
    u32 id=func_0206be2c();
    if(id) {func_0206dcd0(func_02062a10(id));return;}
    func_0206dcd0(func_02062a10(func_0206bf34()));
}
