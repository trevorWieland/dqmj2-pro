/* ov000 row 0x02223190: 80 bytes.
 *
 * What it does: 19 instructions, 2 call(s), 5 load(s), 2 store(s), 2 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x02223190; every literal pool
 * word and branch target is read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_02246574[];
extern void native_fn_0205f5f4(void);
extern void native_fn_020bb38c(void);


asm u32 native_ov000_02223190 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =native_data_02246574
    ldrb r1, [r0, #1]
    cmp r1, #0
    beq ov000_02223190_L044
    sub r1, r1, #1
    strb r1, [r0, #1]
    tst r1, #0xff
    bne ov000_02223190_L044
    ldr r0, [r0, #0xc]
    bl native_fn_0205f5f4
    ldr r0, =native_data_02246574
    mov r1, #2
    strb r1, [r0]
    ldr r0, [r0, #4]
    mov r1, #1
    bl native_fn_020bb38c
ov000_02223190_L044:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
