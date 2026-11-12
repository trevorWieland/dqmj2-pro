/* ov001 row 0x021d97ac: 232 bytes.
 *
 * What it does: 56 instructions; 9 call(s) to 0x021d93f8, 0x02044cdc, 0x021d9424, +6 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (56 instructions, 9 calls, 4 branches, 9 back edges, 2 literal slots).
 *
 *   pool +0xe0 -> constant 0x02236f6c (image word 0x02236f6c)
 *   pool +0xe4 -> constant 0x022362ac (image word 0x022362ac)
 *   branch +0x24 -> +0xd4
 *   branch +0x58 -> +0xd4
 *   branch +0x80 -> +0xc0
 *   branch +0xbc -> +0xc8
 *   test +0x20 cmp r0, #0
 *   test +0x28 cmp r7, #0
 *   test +0x54 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d97ac; the literal pool and
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

extern void native_fn_021d93f8(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021d9424(void);
extern void native_fn_021d9494(void);
extern void native_fn_020449d4(void);
extern void native_fn_02042e30(void);
extern void native_fn_02041e2c(void);
extern void native_fn_02028dcc(void);


asm u32 native_ov001_021d97ac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #8
    mov r5, r2
    mov r7, r0
    add r0, r5, #8
    mov r4, r1
    mov r6, #0
    bl native_fn_021d93f8
    cmp r0, #0
    beq ov001_021d97ac_Ld4
    cmp r7, #0
    ldreq r1, =0x02236f6c
    add r0, r4, r4, lsl #4
    ldrne r1, =0x022362ac
    add r4, r1, r0, lsl #6
    mov r0, r5
    bl native_fn_02044cdc
    mov r2, r0
    mov r0, r4
    add r1, r5, #8
    bl native_fn_021d9424
    cmp r0, #0
    beq ov001_021d97ac_Ld4
    mov r0, r4
    mov r1, #0
    mov r2, #1
    bl native_fn_021d9494
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #17
    movs r0, r0, lsr #31
    beq ov001_021d97ac_Lc0
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    add r1, sp, #4
    add r2, sp, #0
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    and r0, r0, #255
    bl native_fn_02042e30
    ldr r1, [sp, #0x4]
    ldr r2, [sp]
    mov r3, r1
    add r0, r4, #256
    bl native_fn_02041e2c
    b ov001_021d97ac_Lc8
ov001_021d97ac_Lc0:
    add r0, r4, #256
    bl native_fn_02028dcc
ov001_021d97ac_Lc8:
    mov r6, #1
    strb r6, [r4, #0x31c]
    strb r6, [r4, #0x31d]
ov001_021d97ac_Ld4:
    mov r0, r6
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
