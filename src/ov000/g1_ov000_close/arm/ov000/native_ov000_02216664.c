/* ov000 row 0x02216664: 120 bytes.
 *
 * What it does: 30 instructions; 10 call(s) to 0x022166bc, 0x02049ad0, 0x022162c0, +7 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x14 -> +0x58
 *   back edge +0x54 -> +0x18
 *   test +0x10 cmp r0, #0
 *   test +0x50 cmp r1, r0, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02216664; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_022162c0(void);
extern void native_fn_022172dc(void);


asm u32 native_ov000_02216664 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrh r0, [r5, #12]
    mov r4, #0
    cmp r0, #0
    ble ov000_02216664_L58
ov000_02216664_L18:
    add r0, r4, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    bl native_fn_022162c0
    add r0, r4, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    bl native_fn_022162c0
    add r0, r4, #1
    mov r0, r0, lsl #24
    ldrh r1, [r5, #12]
    mov r4, r0, asr #24
    cmp r1, r0, asr #24
    bgt ov000_02216664_L18
ov000_02216664_L58:
    mov r0, #4
    bl native_fn_02049ad0
    bl native_fn_022162c0
    mov r0, #23
    bl native_fn_02049ad0
    bl native_fn_022162c0
    bl native_fn_022172dc
    ldmia sp!, {r3, r4, r5, pc}
}
