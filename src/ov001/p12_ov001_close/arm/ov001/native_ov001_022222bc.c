/* ov001 row 0x022222bc: 184 bytes.
 *
 * What it does: 46 instructions; 7 call(s) to 0x021db8d0, 0x022186d0, 0x021dc1c0, +4 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 7 calls (46 instructions, 7 calls, 5 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x20 -> +0xa0
 *   branch +0x34 -> +0xa0
 *   branch +0x44 -> +0xa0
 *   branch +0x54 -> +0xa0
 *   branch +0x6c -> +0x88
 *   back edge +0x94 -> +0x60
 *   back edge +0xac -> +0x14
 *   test +0x1c cmp r0, #0
 *   test +0x30 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x68 cmp r0, #0
 *   test +0x7c cmp r0, #0
 *   test +0x8c cmp r6, #3
 *   test +0xa4 cmp r6, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022222bc; the literal pool and
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
extern void native_fn_022186d0(void);
extern void native_fn_021dc1c0(void);
extern void native_fn_022185b0(void);


asm u32 native_ov001_022222bc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r4, [r0, #0x8]
    mov r6, #0
    mov r7, r4
    mov r5, #231
ov001_022222bc_L14:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022222bc_La0
    mov r0, r7
    mov r1, r5
    bl native_fn_022186d0
    cmp r0, #0
    beq ov001_022222bc_La0
    add r0, r7, #512
    ldrsb r0, [r0, #84]
    cmp r0, #0
    bne ov001_022222bc_La0
    mov r0, r7
    bl native_fn_021dc1c0
    cmp r0, #0
    beq ov001_022222bc_La0
    mov r6, #0
    mov r5, #3
ov001_022222bc_L60:
    mov r0, r4
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022222bc_L88
    mov r0, r4
    mov r1, r5
    bl native_fn_022185b0
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
ov001_022222bc_L88:
    add r6, r6, #1
    cmp r6, #3
    add r4, r4, #1088
    blt ov001_022222bc_L60
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_022222bc_La0:
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_022222bc_L14
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
