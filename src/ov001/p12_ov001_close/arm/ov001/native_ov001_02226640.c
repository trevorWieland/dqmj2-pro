/* ov001 row 0x02226640: 156 bytes.
 *
 * What it does: 39 instructions; 7 call(s) to 0x02008e0c, 0x02044cdc, 0x02044cdc, +4 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 7 calls (39 instructions, 7 calls, 1 branch, 6 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x5c
 *   back edge +0x68 -> +0x2c
 *   branch +0x7c -> +0x90
 *   test +0x30 cmp r0, #0
 *   test +0x54 cmp r4, r0
 *   test +0x60 cmp r6, #3
 *   test +0x78 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02226640; the literal pool and
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
extern void native_fn_02044cdc(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_02226640 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #12
    mov r8, r1
    mov r7, r2
    add r1, sp, #0
    mov r2, #12
    mov r9, r0
    bl native_fn_02008e0c
    mov r6, #0
    mov r10, r6
    add r5, sp, #0
ov001_02226640_L2c:
    ldr r0, [r5, r6, lsl #2]
    cmp r0, #0
    beq ov001_02226640_L5c
    ldr r0, [r8, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    ldr r1, [r7, #0x1e8]
    mov r4, r0
    ldrsh r0, [r1, #42]
    bl native_fn_02044cdc
    cmp r4, r0
    strne r10, [r5, r6, lsl #2]
ov001_02226640_L5c:
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_02226640_L2c
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02226640_L90
    add r0, sp, #0
    mov r1, r9
    mov r2, #12
    bl native_fn_02008e0c
ov001_02226640_L90:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
