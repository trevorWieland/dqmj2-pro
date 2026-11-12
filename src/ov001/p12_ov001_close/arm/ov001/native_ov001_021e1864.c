/* ov001 row 0x021e1864: 236 bytes.
 *
 * What it does: 59 instructions; 11 call(s) to 0x0207afec, 0x0207afec, 0x021e18d4, +8 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 11 calls (59 instructions, 11 calls, 6 branches, 9 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x70
 *   branch +0x6c -> +0xe0
 *   branch +0x80 -> +0x98
 *   branch +0x94 -> +0xe0
 *   branch +0xa8 -> +0xe0
 *   branch +0xcc -> +0xdc
 *   branch +0xd8 -> +0xe0
 *   test +0x2c cmp r6, #0
 *   test +0x7c cmp r0, #44
 *   test +0xa4 cmp r0, #54
 *   test +0xc8 cmp r4, r0
 *   test +0xd4 cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e1864; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0207afec(void);
extern void native_fn_021f08ec(void);
extern void native_fn_021e1708(void);
extern void native_fn_021e17e4(void);
extern void native_fn_02044cdc(void);
extern void native_fn_020655d8(void);


asm u32 native_ov001_021e1864 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #12
    mov r9, r0
    mov r5, r1
    mov r4, r2
    mov r8, r3
    mov r7, #1
    bl native_fn_0207afec
    mov r0, r9
    bl native_fn_0207afec
    ldrb r6, [r0, #0x1f]
    cmp r6, #0
    ble ov001_021e1864_L70
    mov r0, r4
    mov r1, r9
    bl native_fn_021f08ec
    mov r1, r0
    ldr r0, [sp, #0x28]
    str r8, [sp]
    ldr r12, [sp, #0x2c]
    str r0, [sp, #0x4]
    mov r0, r6
    mov r2, r5
    mov r3, r4
    str r12, [sp, #0x8]
    bl native_fn_021e1708
    mov r7, r0
    b ov001_021e1864_Le0
ov001_021e1864_L70:
    mov r0, r9
    bl native_fn_0207afec
    ldrb r0, [r0, #0x21]
    cmp r0, #44
    bne ov001_021e1864_L98
    mov r0, r5
    mov r1, r4
    bl native_fn_021e17e4
    mov r7, r0
    b ov001_021e1864_Le0
ov001_021e1864_L98:
    mov r0, r9
    bl native_fn_0207afec
    ldrb r0, [r0, #0x21]
    cmp r0, #54
    bne ov001_021e1864_Le0
    ldr r0, [r5, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    ldr r1, [r4, #0x1e8]
    mov r4, r0
    ldrsh r0, [r1, #42]
    bl native_fn_02044cdc
    cmp r4, r0
    bne ov001_021e1864_Ldc
    bl native_fn_020655d8
    cmp r0, #0
    beq ov001_021e1864_Le0
ov001_021e1864_Ldc:
    mov r7, #0
ov001_021e1864_Le0:
    mov r0, r7
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
