/* ov001 row 0x02220dcc: 140 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x021db8d0, 0x02218430, 0x02220e3c, +2 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 5 calls (35 instructions, 5 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x70
 *   branch +0x44 -> +0x70
 *   back edge +0x6c -> +0x48
 *   back edge +0x7c -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x4c cmp r1, #182
 *   test +0x50 cmpne r1, #164
 *   test +0x54 cmpne r1, #180
 *   test +0x68 cmp r2, r0
 *   test +0x74 cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02220dcc; the literal pool and
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
extern void native_fn_02218430(void);


asm u32 native_ov001_02220dcc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #200
    mov r7, #0
    ldr r8, [r0, #0x4]
    add r6, sp, #0
    mov r5, #200
    mov r4, r7
ov001_02220dcc_L1c:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02220dcc_L70
    mov r0, r8
    mov r1, r6
    mov r2, r5
    bl native_fn_02218430
    mov r2, r4
    cmp r0, #0
    ble ov001_02220dcc_L70
ov001_02220dcc_L48:
    ldr r1, [r6, r2, lsl #2]
    cmp r1, #182
    cmpne r1, #164
    cmpne r1, #180
    addeq sp, sp, #200
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    add r2, r2, #1
    cmp r2, r0
    blt ov001_02220dcc_L48
ov001_02220dcc_L70:
    add r7, r7, #1
    cmp r7, #3
    add r8, r8, #1088
    blt ov001_02220dcc_L1c
    mov r0, #0
    add sp, sp, #200
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
