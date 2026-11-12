/* ov001 row 0x02225bac: 184 bytes.
 *
 * What it does: 46 instructions; 7 call(s) to 0x02008e0c, 0x02225c24, 0x02225bf8, +4 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 7 calls (46 instructions, 7 calls, 2 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x78
 *   branch +0x48 -> +0x78
 *   branch +0x58 -> +0x78
 *   back edge +0x74 -> +0x4c
 *   back edge +0x84 -> +0x30
 *   branch +0x98 -> +0xac
 *   test +0x34 cmp r1, #0
 *   test +0x44 cmp r7, #0
 *   test +0x54 cmp r4, r1
 *   test +0x60 cmp lr, r1
 *   test +0x70 cmp lr, r7
 *   test +0x7c cmp r12, #3
 *   test +0x94 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225bac; the literal pool and
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
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_02225bac (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r5, r1
    mov r4, r2
    add r1, sp, #0
    mov r2, #12
    mov r6, r0
    bl native_fn_02008e0c
    mov r12, #0
    mov r0, r12
    add r3, sp, #0
    mov r2, r12
ov001_02225bac_L30:
    ldr r1, [r3, r12, lsl #2]
    cmp r1, #0
    beq ov001_02225bac_L78
    ldrb r7, [r5, #0x323]
    mov lr, r2
    cmp r7, #0
    ble ov001_02225bac_L78
ov001_02225bac_L4c:
    add r1, r5, lr
    ldrb r1, [r1, #0x35e]
    cmp r4, r1
    beq ov001_02225bac_L78
    sub r1, r7, #1
    cmp lr, r1
    streq r0, [r3, r12, lsl #2]
    ldrb r7, [r5, #0x323]
    add lr, lr, #1
    cmp lr, r7
    blt ov001_02225bac_L4c
ov001_02225bac_L78:
    add r12, r12, #1
    cmp r12, #3
    add r5, r5, #1088
    blt ov001_02225bac_L30
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225bac_Lac
    add r0, sp, #0
    mov r1, r6
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225bac_Lac:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
