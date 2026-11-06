typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {u8 phase;u8 pad[3];u32 dirty;u32 values[6];} State;
typedef struct {u8 prefix[620];s8 mode;} Runtime;
typedef struct {s16 x,y;} Position;
extern State data_ov003_021e0670;
extern Runtime *func_02061944(void);
extern void func_ov003_021d9f18(void);
extern void func_ov003_021da01c(void);
extern void func_ov003_021da178(void);
extern void func_ov003_021da378(void);
extern void func_020622ec(u32,u32,u32);
extern void func_02061c1c(s8,u32,u8,u32,u32,u32,u32);
extern void func_02045ed0(u32);
extern void **func_02061dcc(s8);
extern void func_02049f4c(void *);
extern void func_02049ffc(void *);
extern void func_0204aaf0(s8,Position *,u32,u32,u32,u32,u32);
extern void func_0204ab98(s8,Position *,u32,const char *,u32);
extern char data_ov003_021e02fc[];
extern char data_ov003_021e0300[];

extern u16 data_ov003_021e02f0[];
extern u16 data_ov003_021e02e0[];
extern u16 data_ov003_021e02ea[];
extern u16 data_ov003_021e02f6[];
extern u16 data_ov003_021e02e4[];
extern void func_020456ac(u32,u32,u32,u32,u32,u32);

void native_ov003_021d9e58(void) {
    data_ov003_021e0670.dirty=0;
    func_ov003_021d9f18();
    data_ov003_021e0670.phase=0;
}

u32 native_ov003_021d9e80(void) {
    Runtime *runtime=func_02061944();
    u32 result=0;
    switch(data_ov003_021e0670.phase) {
    case 0:func_ov003_021da01c();func_ov003_021da178();data_ov003_021e0670.phase=1;break;
    case 1:
        if(data_ov003_021e0670.dirty) {func_ov003_021da178();data_ov003_021e0670.dirty=0;}
        break;
    }
    if(runtime->mode!=42) result=1;
    return result;
}

void native_ov003_021d9efc(void) {
    func_ov003_021da378();
    func_020622ec(6,20,0);
}

void native_ov003_021d9f18(void) {
    u8 index;
    func_02061c1c(6,2,4,14,2,0,0);
    func_02061c1c(13,16,4,14,2,0,0);
    for(index=0;index<6;index++) func_02061c1c((s8)(index+7),3,(u8)(index*2+8),13,2,0,0);
    for(index=0;index<6;index++) func_02061c1c((s8)(index+14),16,(u8)(index*2+8),13,2,0,0);
    func_02045ed0(1);
}

void native_ov003_021da01c(void) {
    Position position={0,0};
    s8 index;
    for(index=0;index<7;index++) func_02049f4c(func_02061dcc((s8)(index+6)));
    for(index=0;index<7;index++) func_02049ffc(((void **)*func_02061dcc((s8)(index+6)))[1]);
    func_0204aaf0(6,&position,20,0,32,1,1);
    position.x+=104;
    func_0204ab98(6,&position,1,data_ov003_021e02fc,0);
    for(index=0;index<6;index++) {
        position.x=0;
        func_0204aaf0((s8)(index+7),&position,20,0,(u16)(index+33),1,1);
        position.x+=96;
        func_0204ab98((s8)(index+7),&position,1,data_ov003_021e0300,0);
    }
}

void native_ov003_021da178(void) {
    Position position={0,0};
    s8 index;
    for(index=0;index<7;index++) func_02049f4c(func_02061dcc((s8)(index+13)));
    for(index=0;index<7;index++) func_02049ffc(((void **)*func_02061dcc((s8)(index+13)))[1]);
    func_0204aaf0(13,&position,20,0,(u16)(data_ov003_021e0670.values[0]+42),1,1);
    func_0204aaf0(14,&position,20,0,data_ov003_021e02f0[data_ov003_021e0670.values[1]],1,1);
    func_0204aaf0(15,&position,20,0,data_ov003_021e02e0[data_ov003_021e0670.values[2]],1,1);
    func_0204aaf0(16,&position,20,0,data_ov003_021e02ea[data_ov003_021e0670.values[3]],1,1);
    func_0204aaf0(17,&position,20,0,data_ov003_021e02f6[data_ov003_021e0670.values[4]],1,1);
    func_0204aaf0(18,&position,20,0,data_ov003_021e02e4[data_ov003_021e0670.values[5]],1,1);
    func_0204aaf0(19,&position,20,0,61,1,1);
}

void native_ov003_021da378(void) {
    func_020456ac(0,1,0,0,32,24);
    func_020456ac(0,2,0,0,32,24);
}

void native_ov003_021da3d0(void) {
    data_ov003_021e0670.dirty=1;
}
