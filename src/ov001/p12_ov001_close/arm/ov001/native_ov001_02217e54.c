/* ov001 row 0x02217e54: 108 bytes.
 *
 * What it does: 25 instructions; 3 call(s) to 0x021d93f8, 0x021d9424, 0x021d9494; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (25 instructions, 3 calls, 2 branches, 3 back edges, 2 literal slots).
 *
 *   pool +0x64 -> constant 0x02242c50 (image word 0x02242c50)
 *   pool +0x68 -> constant 0x02242c4c (image word 0x02242c4c)
 *   branch +0x18 -> +0x5c
 *   branch +0x30 -> +0x5c
 *   test +0x14 cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02217e54; the literal pool and
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
extern void native_fn_021d9424(void);
extern void native_fn_021d9494(void);


asm u32 native_ov001_02217e54 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    add r0, r5, #1
    mov r4, #0
    bl native_fn_021d93f8
    cmp r0, #0
    beq ov001_02217e54_L5c
    ldr r0, =0x02242c50
    add r1, r5, #1
    mov r2, r4
    bl native_fn_021d9424
    cmp r0, #0
    beq ov001_02217e54_L5c
    ldr r0, =0x02242c50
    mov r1, r4
    mov r2, #1
    bl native_fn_021d9494
    ldr r1, =0x02242c50
    mov r4, #1
    strb r4, [r1, #0x1e8]
    ldr r0, =0x02242c4c
    strb r4, [r1, #0x1e9]
    strb r4, [r0]
ov001_02217e54_L5c:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
