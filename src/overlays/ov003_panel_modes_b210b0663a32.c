typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef struct {u32 words[52];} Payload;
typedef struct {signed char active:1; signed char done:1; signed char changed:1; signed char started:1; signed char running:4;} Flags;
typedef struct {Payload payload; volatile s8 index; Flags flags; u8 reserved[18];} Menu;
typedef struct {u8 prefix[617]; s8 choice; u8 middle[2]; s8 mode; u8 rest[2]; s8 selector;} Runtime;
extern Menu data_ov003_021e058c;
extern u8 data_ov003_021e057c[];
extern u32 data_ov003_021e0580[];
extern Runtime *func_02061944(void);
extern void func_02062328(void);
extern void func_02062144(s8,u32);
extern void func_ov003_021d9e40(void);
extern void func_ov003_021d9634(void *);
extern void func_ov003_021d9984(u32,void *);
extern void func_ov003_021d9cb8(void);
extern void func_ov003_021d9d84(void);
extern Payload *func_0205fc10(void *,void (*)(void),void (*)(void),u32,u32,u32,u32,u32);
extern void func_0205fd0c(void *);
extern u32 func_0206238c(s8 *,u32,u32);
extern void func_020620b4(s8);
extern void func_02062358(u32);
extern void func_ov003_021d9dc0(void);

u32 native_ov003_021d8ddc(void) {
    Runtime *runtime=func_02061944();
    u32 result=0;
    switch(data_ov003_021e057c[2]) {
    case 0:
        func_02062328();
        func_02062144(runtime->selector,0);
        func_ov003_021d9e40();
        func_ov003_021d9634(data_ov003_021e0580);
        func_ov003_021d9984(21,data_ov003_021e0580);
        data_ov003_021e058c.flags.started=1;
        if(runtime->mode==42 && !data_ov003_021e058c.flags.active) {
            data_ov003_021e058c.index=0;
            data_ov003_021e058c.flags.active=1;
            data_ov003_021e058c.flags.done=0;
            data_ov003_021e058c.flags.started=0;
            data_ov003_021e058c.payload=*func_0205fc10(&data_ov003_021e058c,func_ov003_021d9cb8,func_ov003_021d9d84,0,18,8192,2,0);
            func_0205fd0c(&data_ov003_021e058c);
        }
        data_ov003_021e057c[2]=1;
        break;
    case 1: {
        s8 next=35;
        u32 direction=func_0206238c(&next,35,36);
        if(direction!=1) direction=0;
        if(next!=runtime->choice) {
            func_020620b4(next);
            func_02062358(direction);
            result=1;
        }
        break;
    }
    }
    if(runtime->mode!=42) {func_ov003_021d9dc0();result=1;}
    return result;
}

u32 native_ov003_021d8ff4(void) {
    Runtime *runtime=func_02061944();
    u32 result=0;
    switch(data_ov003_021e057c[2]) {
    case 0:
        func_02062328();
        func_02062144(runtime->selector,0);
        func_ov003_021d9e40();
        func_ov003_021d9634(data_ov003_021e0580);
        func_ov003_021d9984(22,data_ov003_021e0580);
        data_ov003_021e058c.flags.started=1;
        if(runtime->mode==42 && !data_ov003_021e058c.flags.active) {
            data_ov003_021e058c.index=0;
            data_ov003_021e058c.flags.active=1;
            data_ov003_021e058c.flags.done=0;
            data_ov003_021e058c.flags.started=0;
            data_ov003_021e058c.payload=*func_0205fc10(&data_ov003_021e058c,func_ov003_021d9cb8,func_ov003_021d9d84,0,18,8192,2,0);
            func_0205fd0c(&data_ov003_021e058c);
        }
        data_ov003_021e057c[2]=1;
        break;
    case 1: {
        s8 next=36;
        u32 direction=func_0206238c(&next,35,36);
        if(direction!=1) direction=0;
        if(next!=runtime->choice) {
            func_020620b4(next);
            func_02062358(direction);
            result=1;
        }
        break;
    }
    }
    if(runtime->mode!=42) {func_ov003_021d9dc0();result=1;}
    return result;
}

u32 native_ov003_021d91f8(void) {
    Runtime *runtime=func_02061944();
    u32 result=0;
    switch(data_ov003_021e057c[2]) {
    case 0:
        func_02062328();
        func_02062144(runtime->selector,0);
        func_ov003_021d9e40();
        func_ov003_021d9634(data_ov003_021e0580);
        func_ov003_021d9984(10,data_ov003_021e0580);
        data_ov003_021e058c.flags.started=1;
        if(runtime->mode==42 && !data_ov003_021e058c.flags.active) {
            data_ov003_021e058c.index=0;
            data_ov003_021e058c.flags.active=1;
            data_ov003_021e058c.flags.done=0;
            data_ov003_021e058c.flags.started=0;
            data_ov003_021e058c.payload=*func_0205fc10(&data_ov003_021e058c,func_ov003_021d9cb8,func_ov003_021d9d84,0,18,8192,2,0);
            func_0205fd0c(&data_ov003_021e058c);
        }
        data_ov003_021e057c[2]=1;
        break;
    case 1: {
        s8 next=37;
        u32 direction=func_0206238c(&next,37,38);
        if(direction!=1) direction=0;
        if(next!=runtime->choice) {
            func_020620b4(next);
            func_02062358(direction);
            result=1;
        }
        break;
    }
    }
    if(runtime->mode!=42) {func_ov003_021d9dc0();result=1;}
    return result;
}

u32 native_ov003_021d93fc(void) {
    Runtime *runtime=func_02061944();
    u32 result=0;
    switch(data_ov003_021e057c[2]) {
    case 0:
        func_02062328();
        func_02062144(runtime->selector,0);
        func_ov003_021d9e40();
        func_ov003_021d9634(data_ov003_021e0580);
        func_ov003_021d9984(11,data_ov003_021e0580);
        data_ov003_021e058c.flags.started=1;
        if(runtime->mode==42 && !data_ov003_021e058c.flags.active) {
            data_ov003_021e058c.index=0;
            data_ov003_021e058c.flags.active=1;
            data_ov003_021e058c.flags.done=0;
            data_ov003_021e058c.flags.started=0;
            data_ov003_021e058c.payload=*func_0205fc10(&data_ov003_021e058c,func_ov003_021d9cb8,func_ov003_021d9d84,0,18,8192,2,0);
            func_0205fd0c(&data_ov003_021e058c);
        }
        data_ov003_021e057c[2]=1;
        break;
    case 1: {
        s8 next=38;
        u32 direction=func_0206238c(&next,37,38);
        if(direction!=1) direction=0;
        if(next!=runtime->choice) {
            func_020620b4(next);
            func_02062358(direction);
            result=1;
        }
        break;
    }
    }
    if(runtime->mode!=42) {func_ov003_021d9dc0();result=1;}
    return result;
}
