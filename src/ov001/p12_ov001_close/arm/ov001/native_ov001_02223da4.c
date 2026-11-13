/* ov001 row 0x02223da4: 144 bytes.
 *
 * What it does: 36 instructions; 6 call(s) to 0x021db8d0, 0x02218430, 0x02223e18, +3 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 6 calls (36 instructions, 6 calls, 1 branch, 5 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x74
 *   branch +0x48 -> +0x74
 *   back edge +0x70 -> +0x4c
 *   back edge +0x80 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x44 cmp r9, #0
 *   test +0x58 cmp r0, #0
 *   test +0x6c cmp r8, r9
 *   test +0x78 cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02223da4; the literal pool and
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
extern void native_fn_0207afec(void);


asm u32 native_ov001_02223da4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #200
    mov r7, #0
    ldr r10, [r0, #0x8]
    add r6, sp, #0
    mov r5, #200
    mov r4, r7
ov001_02223da4_L1c:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02223da4_L74
    mov r0, r10
    mov r1, r6
    mov r2, r5
    bl native_fn_02218430
    mov r9, r0
    mov r8, r4
    cmp r9, #0
    ble ov001_02223da4_L74
ov001_02223da4_L4c:
    ldr r0, [r6, r8, lsl #2]
    bl native_fn_0207afec
    ldrb r0, [r0, #0x1f]
    cmp r0, #0
    addne sp, sp, #200
    movne r0, #0
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    add r8, r8, #1
    cmp r8, r9
    blt ov001_02223da4_L4c
ov001_02223da4_L74:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_02223da4_L1c
    mov r0, #1
    add sp, sp, #200
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
