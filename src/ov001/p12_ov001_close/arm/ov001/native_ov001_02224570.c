/* ov001 row 0x02224570: 204 bytes.
 *
 * What it does: 51 instructions; 8 call(s) to 0x02008e0c, 0x022244a0, 0x022245a0, +5 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 8 calls (51 instructions, 8 calls, 2 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x50
 *   back edge +0x5c -> +0x30
 *   branch +0x74 -> +0x8c
 *   back edge +0x98 -> +0x6c
 *   branch +0xac -> +0xc0
 *   test +0x34 cmp r0, #0
 *   test +0x48 cmp r0, r9
 *   test +0x54 cmp r8, #3
 *   test +0x70 cmp r0, #0
 *   test +0x84 cmp r0, r9
 *   test +0x90 cmp r8, #3
 *   test +0xa8 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02224570; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_022244a0(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_02224570 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #12
    mov r5, r1
    mov r4, r2
    add r1, sp, #0
    mov r2, #12
    mov r6, r0
    mov r9, #0
    bl native_fn_02008e0c
    mov r10, r5
    mov r8, r9
    add r7, sp, #0
ov001_02224570_L30:
    ldr r0, [r7, r8, lsl #2]
    cmp r0, #0
    beq ov001_02224570_L50
    mov r0, r10
    mov r1, r4
    bl native_fn_022244a0
    cmp r0, r9
    movgt r9, r0
ov001_02224570_L50:
    add r8, r8, #1
    cmp r8, #3
    add r10, r10, #1088
    blt ov001_02224570_L30
    mov r8, #0
    mov r10, r8
    add r7, sp, #0
ov001_02224570_L6c:
    ldr r0, [r7, r8, lsl #2]
    cmp r0, #0
    beq ov001_02224570_L8c
    mov r0, r5
    mov r1, r4
    bl native_fn_022244a0
    cmp r0, r9
    strlt r10, [r7, r8, lsl #2]
ov001_02224570_L8c:
    add r8, r8, #1
    cmp r8, #3
    add r5, r5, #1088
    blt ov001_02224570_L6c
    add r0, sp, #0
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02224570_Lc0
    add r0, sp, #0
    mov r1, r6
    mov r2, #12
    bl native_fn_02008e0c
ov001_02224570_Lc0:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
