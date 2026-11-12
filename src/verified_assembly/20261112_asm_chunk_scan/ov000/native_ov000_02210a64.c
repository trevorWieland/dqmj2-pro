/* ov000 row 0x02210a64: 268 bytes.
 *
 * What it does: Copies a 3-register block to an optional destination under a condition in 2 predicated moves.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x104 -> constant 0x02238634 (image word 0x02238634)
 *   pool +0x108 -> native_data_0222f810 (image word 0x0222f810)
 *   branch +0x38 -> +0xec
 *   branch +0x48 -> +0xec
 *   branch +0x58 -> +0xec
 *   branch +0xbc -> +0xec
 *   branch +0xe8 -> +0xfc
 *   back edge +0xf8 -> +0x20
 *   test +0x24 cmp r0, #0
 *   test +0x2c cmpne r0, #0
 *   test +0x34 cmpne r0, #0
 *   test +0x54 cmp r0, #0
 *   test +0xc4 cmp r9, #0
 *   test +0xd8 cmp r11, #0
 *   test +0xf0 cmp r7, #48
 *   4 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02210a64; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_022109b8(void);
extern void native_fn_020c58c0(void);
extern void native_fn_020449d4(void);
extern void native_fn_022109d8(void);
extern u8 native_data_0222f810[];


asm u32 native_ov000_02210a64 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r3, #0
    ldr r8, =0x02238634
    str r3, [sp]
    mov r10, r0
    mov r9, r1
    mov r11, r2
    mov r7, r3
ov000_02210a64_L20:
    ldrb r0, [r8, #0x274]
    cmp r0, #0
    ldrneb r0, [r8, #0x1e2]
    cmpne r0, #0
    ldrneb r0, [r8, #0x160]
    cmpne r0, #0
    beq ov000_02210a64_Lec
    ldrb r0, [r8, #0x2c2]
    mov r0, r0, lsl #28
    movs r0, r0, lsr #28
    bne ov000_02210a64_Lec
    ldrb r0, [r8, #0x278]
    bl native_fn_022109b8
    cmp r0, #0
    beq ov000_02210a64_Lec
    add r0, r8, #512
    ldrsh r0, [r0, #118]
    ldr r5, [r8, #0x74]
    ldr r3, [r8, #0x70]
    ldmia r10, {r4, r6}
    sub r6, r6, r5
    ldr r2, [r10, #0x8]
    ldr r1, [r8, #0x78]
    sub r5, r4, r3
    sub r4, r2, r1
    bl native_fn_020c58c0
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    and r0, r0, #255
    bl native_fn_022109d8
    smull r3, r2, r6, r6
    smlal r3, r2, r5, r5
    smlal r3, r2, r4, r4
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    subs r0, r3, r0
    rscs r0, r1, r2, asr #12
    bge ov000_02210a64_Lec
    ldr r0, =native_data_0222f810
    cmp r9, #0
    strb r7, [r0]
    addne r0, r8, #112
    ldmneia r0, {r0, r1, r2}
    stmneia r9, {r0, r1, r2}
    cmp r11, #0
    ldrne r0, [r8, #0x8c]
    str r8, [sp]
    strne r0, [r11]
    b ov000_02210a64_Lfc
ov000_02210a64_Lec:
    add r7, r7, #1
    cmp r7, #48
    add r8, r8, #708
    blt ov000_02210a64_L20
ov000_02210a64_Lfc:
    ldr r0, [sp]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
