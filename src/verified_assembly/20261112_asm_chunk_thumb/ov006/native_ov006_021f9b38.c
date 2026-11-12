/* ov006 row 0x021f9b38: 112 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (2 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x5c -> native_data_0220b6b4 (image word 0x0220b6b4)
 *   pool +0x60 -> native_data2_0221c0e4 (image word 0x0221c0e4)
 *   pool +0x64 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   pool +0x68 -> native_fn_021f965c+1 (image word 0x021f965d)
 *   pool +0x6c -> native_fn_021f99d0+1 (image word 0x021f99d1)
 *   branch +0x1a -> +0x58
 *   branch +0x24 -> +0x3a
 *   test +0x18 cmp r0, #0x0
 *   test +0x22 cmp r0, #0x0
 *   4 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9b38; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 112 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b6b4[];
extern void native_fn_02200584(void);
extern u8 native_data2_0221c0e4[];
extern void native_fn_021f965c(void);
extern void native_fn_021f52cc(void);
extern void native_fn_021f530c(void);
extern void native_fn_021f99d0(void);


asm u32 native_ov006_021f9b38 (register u32 a0)
{
    push {r3, lr}
    sub sp, #0x18
    ldr r3, =native_data_0220b6b4
    add r2, sp, #0x4
    ldmia r3!, {r0, r1}
    stmia r2!, {r0, r1}
    ldmia r3!, {r0, r1}
    stmia r2!, {r0, r1}
    ldr r0, [r3, #0]
    str r0, [r2, #0]
    bl native_fn_02200584
    cmp r0, #0x0
    bne ov006_021f9b38_L58
    ldr r0, =native_data2_0221c0e4
    ldr r1, [r0, #0]
    ldrb r0, [r1, #0x15]
    cmp r0, #0x0
    bne ov006_021f9b38_L3a
    ldr r2, [r1, #0x4]
    ldr r0, =0xc1fffcff
    ldr r1, [r2, #0]
    and r0, r1
    str r0, [r2, #0]
    ldr r0, =native_fn_021f965c+1
    bl native_fn_021f52cc
    add sp, #0x18
    pop {r3, pc}
ov006_021f9b38_L3a:
    add r0, sp, #0x0
    mov r1, #0x0
    bl native_fn_021f530c
    ldr r0, =native_data2_0221c0e4
    ldr r1, [sp]
    ldr r0, [r0, #0]
    lsl r2, r1, #0x2
    add r1, sp, #0x4
    ldr r1, [r1, r2]
    add r0, #0x8
    blx r1
    ldr r0, =native_fn_021f99d0+1
    bl native_fn_021f52cc
ov006_021f9b38_L58:
    add sp, #0x18
    pop {r3, pc}
}
