typedef unsigned int u32;
typedef unsigned char u8;

u32 native_ov004_021d8908(void){return 0xAA65;}

u32 native_ov004_021d8914(void){return 0xA99F;}

u32 native_ov004_021d7de8(u32 instruction){
    u8 opcode=instruction>>24;
    if((opcode&14)==10){if((opcode&240)==240)return 1;if(opcode&1)return 2;return 3;}
    return 0;
}
