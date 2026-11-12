/* ov001 row 0x02225534: 204 bytes.
 *
 * What it does: 51 instructions; 6 call(s) to 0x02008e0c, 0x02225564, 0x022255a0, +3 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 6 calls (51 instructions, 6 calls, 2 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x50
 *   back edge +0x5c -> +0x30
 *   branch +0x74 -> +0x8c
 *   back edge +0x98 -> +0x6c
 *   branch +0xac -> +0xc0
 *   test +0x34 cmp r0, #0
 *   test +0x48 cmp r0, r4
 *   test +0x54 cmp r2, #3
 *   test +0x70 cmp r1, #0
 *   test +0x84 cmp r1, r4
 *   test +0x90 cmp r3, #3
 *   test +0xa8 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225534; the literal pool and
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
extern void native_fn_02223f20(void);


asm u32 native_ov001_02225534 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r6, r1
    mov r5, r2
    add r1, sp, #0
    mov r2, #12
    mov r7, r0
    mov r4, #7
    bl native_fn_02008e0c
    mov r3, r6
    mov r2, #0
    add r1, sp, #0
ov001_02225534_L30:
    ldr r0, [r1, r2, lsl #2]
    cmp r0, #0
    beq ov001_02225534_L50
    ldr r0, [r3, #0x1e8]
    add r0, r5, r0
    ldrb r0, [r0, #0x86]
    cmp r0, r4
    movlt r4, r0
ov001_02225534_L50:
    add r2, r2, #1
    cmp r2, #3
    add r3, r3, #1088
    blt ov001_02225534_L30
    mov r3, #0
    mov r0, r3
    add r2, sp, #0
ov001_02225534_L6c:
    ldr r1, [r2, r3, lsl #2]
    cmp r1, #0
    beq ov001_02225534_L8c
    ldr r1, [r6, #0x1e8]
    add r1, r5, r1
    ldrb r1, [r1, #0x86]
    cmp r1, r4
    strgt r0, [r2, r3, lsl #2]
ov001_02225534_L8c:
    add r3, r3, #1
    cmp r3, #3
    add r6, r6, #1088
    blt ov001_02225534_L6c
    add r0, sp, #0
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225534_Lc0
    add r0, sp, #0
    mov r1, r7
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225534_Lc0:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
