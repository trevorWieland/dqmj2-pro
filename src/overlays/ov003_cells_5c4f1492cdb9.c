typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef struct { u8 bytes[12]; } Cell;
typedef struct { u8 prefix[16]; Cell cells[49]; } Runtime;
extern u8 data_ov003_021e0464[];
extern u32 data_ov003_021e0468[];
extern u32 data_ov003_021e0474[];
extern u32 data_ov003_021e0480[];
extern u32 data_ov003_021e048c[];
extern Runtime *func_02061944(void);
extern u8 *func_02062a10(u32);
extern u32 func_02044cdc(s16);
extern void func_ov003_021d87c8(s8,s8,s8,u32);
extern u32 **func_02061dcc(s8);
extern void func_02049f4c(void *);
extern void func_02049ffc(u32);
extern u32 func_02062aa0(void);
extern u32 func_02062ad0(void);
extern u32 func_020c385c(void);
extern u32 func_020c3938(void);
extern void func_0204aaf0(u32,void *,u32,u32,u32,u32,u32);
extern void func_02065818(void *,s8,s8);
extern void func_020456ac(u32,u32,u32,u32,u32,u32);
extern u32 *func_02062a50(u32);
extern u32 *func_02062a88(u32);
extern u32 func_020c3828(u32);
extern u32 func_020c3904(u32);

u8 native_ov003_021d85e4(u32 id,s8 *x,s8 *y,u32 flag) {
    u8 *record;
    u8 index;
    u32 count;
    func_02061944();
    record=func_02062a10(id);
    if (!record) return 0;
    count=func_02044cdc(*(s16 *)(record+24));
    index=0;
    do {
        func_ov003_021d87c8((s8)(data_ov003_021e0464[1]+3+index),*x,*y,flag);
        *y=*y+5;
        index++;
    } while(index<=count);
    *y=*y+1;
    return index;
}

void native_ov003_021d867c(void) {
    s16 position[2]={0,0};
    s8 index;
    for(index=0;index<4;index++) func_02049f4c(func_02061dcc((s8)(index+6)));
    for(index=0;index<4;index++) func_02049ffc((*func_02061dcc((s8)(index+6)))[1]);
    if(!func_02062aa0()) func_0204aaf0(6,position,20,0,7,1,1);
    if(!func_02062ad0()) func_0204aaf0(7,position,20,0,7,1,1);
    if(!func_020c385c()) func_0204aaf0(8,position,20,0,7,1,1);
    if(!func_020c3938()) func_0204aaf0(9,position,20,0,7,1,1);
}

void native_ov003_021d87c8(u32 id,s8 x,s8 y,u32 flag) {
    Runtime *runtime=func_02061944();
    u32 offset=id*12;
    Cell *cells=runtime->cells;
    switch(id) {
    case 3:case 4:case 5:case 6:case 7:case 8:case 9:case 10:case 11:case 12:case 13:case 14:
        if(flag) native_ov003_021d87c8(1,x,y,1);
        else native_ov003_021d87c8(2,x,y,0);
        func_02065818((u8 *)cells+offset,x,y);
        break;
    default: func_02065818((u8 *)cells+offset,x,y); break;
    }
}

void native_ov003_021d8890(void) {
    func_020456ac(0,1,0,0,32,24);
    func_020456ac(0,2,0,0,32,24);
}

void native_ov003_021d88e8(void) {
    u8 index;
    u32 *record;
    for(index=0;index<3;index++) {
        data_ov003_021e0468[index]=-1;
        data_ov003_021e0474[index]=-1;
        data_ov003_021e048c[index]=-1;
        data_ov003_021e0480[index]=-1;
    }
    for(index=0;index<3;index++) {
        record=func_02062a50(index);
        if(record) data_ov003_021e0468[index]=record[5];
    }
    for(index=0;index<3;index++) {
        record=func_02062a88(index);
        if(record) data_ov003_021e0474[index]=record[5];
    }
    for(index=0;index<3;index++) data_ov003_021e048c[index]=func_020c3828(index);
    for(index=0;index<3;index++) data_ov003_021e0480[index]=func_020c3904(index);
}
