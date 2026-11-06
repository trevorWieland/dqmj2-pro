typedef unsigned char u8;
typedef unsigned short u16;
void native_utility_child_arm9_main_0200ab14(u16 value, void *destination, int bytes) {
    int offset = 0;
for(;;) { if(offset >= bytes) return; *(u16 *)((u8 *)destination + offset) = value; offset += 2; }
}
