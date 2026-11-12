/* ov006 row 0x021e9550: 140 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> native_data_02208300 (image word 0x02208300)
 *   pool +0x88 -> native_data_02208358 (image word 0x02208358)
 *   branch +0x54 -> +0x6c
 *   branch +0x60 -> +0x74
 *   test +0x50 cmp r4, #0
 *   test +0x58 cmp r4, #14
 *   test +0x5c cmpne r4, #86
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e9550; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021e6488(void);
extern void native_fn_021eb9a4(void);
extern u8 native_data_02208300[];
extern u8 native_data_02208358[];
extern void native_fn_021e81e8(void);
extern void native_fn_021ebb08(void);
extern void native_fn_021e7a18(void);


asm u32 native_ov006_021e9550 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #20
    mov r4, r0
    bl native_fn_021e6488
    mov r0, #3
    mov r1, #0
    mov r2, #1
    bl native_fn_021eb9a4
    mov r0, #28
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    str r12, [sp, #0xc]
    ldr r1, =native_data_02208300
    ldr r3, =native_data_02208358
    mov r2, #5
    str r12, [sp, #0x10]
    bl native_fn_021e81e8
    cmp r4, #0
    beq ov006_021e9550_L6c
    cmp r4, #14
    cmpne r4, #86
    beq ov006_021e9550_L74
    add sp, sp, #20
    ldmia sp!, {r3, r4, pc}
ov006_021e9550_L6c:
    mov r0, #0
    bl native_fn_021ebb08
ov006_021e9550_L74:
    mov r0, #0
    bl native_fn_021e7a18
    add sp, sp, #20
    ldmia sp!, {r3, r4, pc}
}
