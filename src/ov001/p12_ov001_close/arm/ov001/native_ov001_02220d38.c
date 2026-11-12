/* ov001 row 0x02220d38: 148 bytes.
 *
 * What it does: 37 instructions; 5 call(s) to 0x021db8d0, 0x02218430, 0x02220db0, +2 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 5 calls (37 instructions, 5 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x78
 *   branch +0x38 -> +0x78
 *   branch +0x54 -> +0x78
 *   back edge +0x74 -> +0x58
 *   back edge +0x84 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x5c cmp r1, #119
 *   test +0x70 cmp r2, r0
 *   test +0x7c cmp r4, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02220d38; the literal pool and
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
extern void native_fn_02218430(void);


asm u32 native_ov001_02220d38 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #200
    mov r4, #0
    ldr r5, [r0, #0x8]
    add r8, sp, #0
    mov r7, #200
    mov r6, r4
ov001_02220d38_L1c:
    mov r0, r5
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02220d38_L78
    add r0, r5, #512
    ldrsb r0, [r0, #68]
    cmp r0, #0
    bne ov001_02220d38_L78
    mov r0, r5
    mov r1, r8
    mov r2, r7
    bl native_fn_02218430
    mov r2, r6
    cmp r0, #0
    ble ov001_02220d38_L78
ov001_02220d38_L58:
    ldr r1, [r8, r2, lsl #2]
    cmp r1, #119
    addeq sp, sp, #200
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    add r2, r2, #1
    cmp r2, r0
    blt ov001_02220d38_L58
ov001_02220d38_L78:
    add r4, r4, #1
    cmp r4, #3
    add r5, r5, #1088
    blt ov001_02220d38_L1c
    mov r0, #0
    add sp, sp, #200
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
