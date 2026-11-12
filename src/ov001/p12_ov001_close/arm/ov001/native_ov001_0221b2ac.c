/* ov001 row 0x0221b2ac: 144 bytes.
 *
 * What it does: 36 instructions; 5 call(s) to 0x021db8d0, 0x02065d88, 0x0221b2c8, +2 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 5 calls (36 instructions, 5 calls, 2 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x40
 *   back edge +0x4c -> +0x1c
 *   branch +0x54 -> +0x88
 *   back edge +0x78 -> +0x5c
 *   test +0x24 cmp r0, #0
 *   test +0x38 cmp r0, #4
 *   test +0x44 cmp r5, #3
 *   test +0x50 cmp r7, #0
 *   test +0x64 cmp r0, #0
 *   test +0x70 cmp r4, #3
 *   test +0x7c cmp r6, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221b2ac; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_02065d88(void);


asm u32 native_ov001_0221b2ac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r6, #0
    ldr r8, [r0, #0x8]
    ldr r9, [r0, #0x4]
    mov r7, r6
    mov r5, r6
    mov r4, #1
ov001_0221b2ac_L1c:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221b2ac_L40
    ldrb r0, [r9, #0x1fd]
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2d]
    cmp r0, #4
    moveq r7, r4
ov001_0221b2ac_L40:
    add r5, r5, #1
    cmp r5, #3
    add r9, r9, #1088
    blt ov001_0221b2ac_L1c
    cmp r7, #0
    beq ov001_0221b2ac_L88
    mov r4, #0
ov001_0221b2ac_L5c:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    add r4, r4, #1
    addne r6, r6, #1
    cmp r4, #3
    add r8, r8, #1088
    blt ov001_0221b2ac_L5c
    cmp r6, #2
    movge r0, #1
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_0221b2ac_L88:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
