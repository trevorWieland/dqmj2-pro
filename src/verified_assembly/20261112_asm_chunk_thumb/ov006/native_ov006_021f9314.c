/* ov006 row 0x021f9314: 112 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x5c -> native_data_0220b65c (image word 0x0220b65c)
 *   pool +0x60 -> native_data2_0221c0e0 (image word 0x0221c0e0)
 *   pool +0x64 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   pool +0x68 -> native_fn_021f8ed4+1 (image word 0x021f8ed5)
 *   pool +0x6c -> native_fn_021f913c+1 (image word 0x021f913d)
 *   branch +0x14 -> +0x56
 *   branch +0x22 -> +0x38
 *   test +0x12 cmp r0, #0x0
 *   test +0x20 cmp r0, #0x0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9314; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 15 of 112 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b65c[];
extern void native_fn_02200584(void);
extern u8 native_data2_0221c0e0[];
extern void native_fn_021f8ed4(void);
extern void native_fn_021f52cc(void);
extern void native_fn_021f530c(void);
extern void native_fn_021f913c(void);


asm u32 native_ov006_021f9314 (register u32 a0)
{
    push {lr}
    sub sp, #0xc
    ldr r0, =native_data_0220b65c
    ldr r1, [r0, #0x10]
    ldr r0, [r0, #0x14]
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    bl native_fn_02200584
    cmp r0, #0x0
    bne ov006_021f9314_L56
    ldr r0, =native_data2_0221c0e0
    ldr r1, [r0, #0]
    add r0, r1, #0x0
    add r0, #0x2a
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021f9314_L38
    ldr r2, [r1, #0x4]
    ldr r0, =0xc1fffcff
    ldr r1, [r2, #0]
    and r0, r1
    str r0, [r2, #0]
    ldr r0, =native_fn_021f8ed4+1
    bl native_fn_021f52cc
    add sp, #0xc
    pop {pc}
ov006_021f9314_L38:
    add r0, sp, #0x0
    mov r1, #0x0
    bl native_fn_021f530c
    ldr r0, =native_data2_0221c0e0
    ldr r1, [sp]
    ldr r0, [r0, #0]
    lsl r2, r1, #0x2
    add r1, sp, #0x4
    ldr r1, [r1, r2]
    add r0, #0x8
    blx r1
    ldr r0, =native_fn_021f913c+1
    bl native_fn_021f52cc
ov006_021f9314_L56:
    add sp, #0xc
    pop {pc}
    mov r8, r8
}
