typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef struct { signed char active:1; signed char done:1; signed char changed:1; signed char started:1; signed char running:4; } Flags;
typedef struct { u8 prefix[200]; u32 allocation; s8 heap; u8 pad[4]; Flags flags; } Menu;
extern Menu data_ov003_021e0498;
extern u8 data_ov003_021e0464[];
extern u32 data_ov003_021e0468[];
extern u32 data_ov003_021e0474[];
extern u32 data_ov003_021e0480[];
extern u32 data_ov003_021e048c[];
extern void func_ov003_021d82f4(u32);
extern u8 func_ov003_021d85e4(u32,s8 *,s8 *,u32);
extern void func_0205fd18(void);
extern void func_ov003_021d8890(void);
extern void func_0202a498(s8,void *);
extern void func_0205fd4c(u32,u32);
extern void func_0205fd34(void *,u32);
extern u32 func_0205fd28(void *);
extern void func_0205fd0c(void *);

void native_ov003_021d89d8(void) {
    u8 stop=0;
    u8 index;
    s8 x;
    s8 y;
    s8 otherx;
    s8 othery;
    s8 lowerx;
    s8 lowery;
    s8 otherlowerx;
    s8 otherlowery;
    data_ov003_021e0498.flags.running=1;
    x=9;y=4;otherx=18;othery=4;
    for(index=0;index<3;index++) {
        func_ov003_021d82f4(data_ov003_021e0468[index]);
        if(!data_ov003_021e0498.flags.running) break;
        data_ov003_021e0498.flags.changed=1;
        func_0205fd18();
        if(data_ov003_021e0498.flags.started) {stop=1;break;}
        data_ov003_021e0464[1]+=func_ov003_021d85e4(data_ov003_021e0468[index],&x,&y,1);
    }
    if(!stop) for(index=0;index<3;index++) {
        func_ov003_021d82f4(data_ov003_021e048c[index]);
        if(!data_ov003_021e0498.flags.running) break;
        data_ov003_021e0498.flags.changed=1;
        func_0205fd18();
        if(data_ov003_021e0498.flags.started) {stop=1;break;}
        data_ov003_021e0464[1]+=func_ov003_021d85e4(data_ov003_021e048c[index],&otherx,&othery,0);
    }
    lowerx=3;lowery=6;otherlowerx=24;otherlowery=6;
    if(!stop) for(index=0;index<3;index++) {
        func_ov003_021d82f4(data_ov003_021e0474[index]);
        if(!data_ov003_021e0498.flags.running) break;
        data_ov003_021e0498.flags.changed=1;
        func_0205fd18();
        if(data_ov003_021e0498.flags.started) {stop=1;break;}
        data_ov003_021e0464[1]+=func_ov003_021d85e4(data_ov003_021e0474[index],&lowerx,&lowery,1);
    }
    if(!stop) for(index=0;index<3;index++) {
        func_ov003_021d82f4(data_ov003_021e0480[index]);
        if(!data_ov003_021e0498.flags.running) break;
        data_ov003_021e0498.flags.changed=1;
        func_0205fd18();
        if(data_ov003_021e0498.flags.started) {stop=1;break;}
        data_ov003_021e0464[1]+=func_ov003_021d85e4(data_ov003_021e0480[index],&otherlowerx,&otherlowery,0);
    }
    if(stop) {
        data_ov003_021e0498.flags.started=0;
        func_ov003_021d8890();
    }
    data_ov003_021e0498.flags.changed=0;
    data_ov003_021e0498.flags.done=1;
}

void native_ov003_021d8cac(void) {
    data_ov003_021e0498.flags.active=0;
    if(data_ov003_021e0498.allocation) func_0202a498(data_ov003_021e0498.heap,(void *)data_ov003_021e0498.allocation);
    func_0205fd4c(0,0);
}

void native_ov003_021d8ce8(void) {
    if(!data_ov003_021e0498.flags.active) return;
    data_ov003_021e0498.flags.running=0;
    data_ov003_021e0498.flags.started=0;
    func_0205fd34(&data_ov003_021e0498,16);
    while(!func_0205fd28(&data_ov003_021e0498)) {
        data_ov003_021e0498.flags.running=0;
        data_ov003_021e0498.flags.started=0;
        func_0205fd0c(&data_ov003_021e0498);
    }
}
