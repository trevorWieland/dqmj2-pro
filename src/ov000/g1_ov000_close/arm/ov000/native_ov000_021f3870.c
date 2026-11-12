/* ov000 row 0x021f3870: 148 bytes.
 *
 * What it does: 37 instructions; 5 call(s) to 0x021f38f8, 0x02042b3c, 0x02042cb8, +2 more; loops (back edge at +0x20); returns through pop {r4, r5, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x18 -> +0x88
 *   branch +0x28 -> +0x58
 *   branch +0x34 -> +0x58
 *   branch +0x44 -> +0x58
 *   branch +0x5c -> +0x70
 *   test +0x14 cmp r1, #0
 *   test +0x30 cmp r0, #0
 *   test +0x40 tst r0, #8
 *   test +0x58 cmp r4, #0
 *   4 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f3870; the literal pool and
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

extern void native_fn_02042b3c(void);
extern void native_fn_02042cb8(void);
extern void native_fn_021f368c(void);
extern void native_fn_021f36f8(void);


asm u32 native_ov000_021f3870 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    mov r5, r0
    ldr r1, [r5, #0x164]
    mov r4, #0
    cmp r1, #0
    ble ov000_021f3870_L88
    add r1, sp, #0
    bl native_fn_02042b3c
    movs r4, r0
    beq ov000_021f3870_L58
    ldrb r0, [r5, #0x274]
    cmp r0, #0
    bne ov000_021f3870_L58
    ldr r0, [r5, #0x164]
    bl native_fn_02042cb8
    tst r0, #8
    beq ov000_021f3870_L58
    add r1, sp, #0
    mov r0, r5
    bl native_fn_021f368c
    mov r4, r0
ov000_021f3870_L58:
    cmp r4, #0
    beq ov000_021f3870_L70
    add r0, sp, #0
    add r3, r5, #112
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021f3870_L70:
    add r0, r5, #112
    add r3, r5, #272
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, r5
    bl native_fn_021f36f8
ov000_021f3870_L88:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
