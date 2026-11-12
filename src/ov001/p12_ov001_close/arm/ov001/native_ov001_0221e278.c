/* ov001 row 0x0221e278: 172 bytes.
 *
 * What it does: 42 instructions; 5 call(s) to 0x021db8d0, 0x0221e2b8, 0x0221e298, +2 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (42 instructions, 5 calls, 1 branch, 4 back edges, 1 literal slot).
 *
 *   pool +0xa8 -> constant 0x92492493 (image word 0x92492493)
 *   branch +0x2c -> +0x70
 *   back edge +0x54 -> +0x40
 *   back edge +0x7c -> +0x20
 *   branch +0x84 -> +0x98
 *   test +0x28 cmp r0, #0
 *   test +0x48 cmp r1, #29
 *   test +0x74 cmp r7, #3
 *   test +0x80 cmp r9, #0
 *   test +0x98 cmp r8, #4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221e278; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_02026144(void);


asm u32 native_ov001_0221e278 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r8, #0
    ldr r10, [r0, #0x4]
    ldr r4, =0x92492493
    mov r9, r8
    mov r7, r8
    mov r6, r8
    mov r5, #1
ov001_0221e278_L20:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221e278_L70
    ldr r0, [r10, #0x1e8]
    mov r2, r6
    mov r1, r5
    add r3, r0, #1
ov001_0221e278_L40:
    ldrb r0, [r3, #0x86]
    add r1, r1, #1
    cmp r1, #29
    add r2, r2, r0
    add r3, r3, #1
    blt ov001_0221e278_L40
    smull r0, r1, r4, r2
    add r1, r2, r1
    mov r0, r2, lsr #31
    add r1, r0, r1, asr #4
    add r8, r8, r1
    add r9, r9, #1
ov001_0221e278_L70:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_0221e278_L20
    cmp r9, #0
    ble ov001_0221e278_L98
    mov r0, r8
    mov r1, r9
    bl native_fn_02026144
    mov r8, r0
ov001_0221e278_L98:
    cmp r8, #4
    movlt r0, #1
    movge r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
