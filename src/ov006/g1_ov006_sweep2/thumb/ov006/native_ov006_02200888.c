/* ov006 row 0x02200888: 70 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x12 -> +0x42
 *   branch +0x24 -> +0x2e
 *   branch +0x28 -> +0x2e
 *   branch +0x2c -> +0x32
 *   back edge +0x40 -> +0x14
 *   test +0x10 cmp r7, #0x0
 *   test +0x22 cmp r0, r6
 *   test +0x26 cmp r0, #0xc0
 *   test +0x3e cmp r4, r7
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200888; the literal pool and
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

extern void native_fn_02202dc8(void);
extern void native_fn_02202f98(void);
extern void native_fn_02202dcc(void);


asm u32 native_ov006_02200888 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    add r5, r0, #0x0
    add r6, r1, #0x0
    bl native_fn_02202dc8
    add r7, r0, #0x0
    mov r4, #0x0
    cmp r7, #0x0
    ble ov006_02200888_L42
ov006_02200888_L14:
    add r0, r5, #0x0
    add r1, r4, #0x0
    add r2, sp, #0x4
    add r3, sp, #0x0
    bl native_fn_02202f98
    ldr r0, [sp]
    cmp r0, r6
    blt ov006_02200888_L2e
    cmp r0, #0xc0
    bge ov006_02200888_L2e
    mov r2, #0x0
    b ov006_02200888_L32
ov006_02200888_L2e:
    mov r2, #0x2
    lsl r2, r2, #0x8
ov006_02200888_L32:
    add r0, r5, #0x0
    add r1, r4, #0x0
    mov r3, #0x0
    bl native_fn_02202dcc
    add r4, r4, #0x1
    cmp r4, r7
    blt ov006_02200888_L14
ov006_02200888_L42:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
