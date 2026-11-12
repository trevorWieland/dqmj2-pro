/* ov001 row 0x0221ed14: 96 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x021dbec8, 0x0207b004, 0x0203d294; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 3 calls (24 instructions, 3 calls, 3 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x58
 *   branch +0x3c -> +0x50
 *   branch +0x4c -> +0x58
 *   test +0x24 cmp r0, #0
 *   test +0x30 cmpne r0, #0
 *   test +0x38 cmp r4, #0
 *   test +0x48 cmp r0, #9
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221ed14; the literal pool and
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

extern void native_fn_021dbec8(void);
extern void native_fn_0207b004(void);
extern void native_fn_0203d294(void);


asm u32 native_ov001_0221ed14 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r5, [r0]
    ldr r6, [r0, #0xc]
    mov r0, r5
    bl native_fn_021dbec8
    mov r4, r0
    mov r0, r6
    mov r1, #33554432
    bl native_fn_0207b004
    cmp r0, #0
    addne r0, r5, #512
    ldrnesb r0, [r0, #85]
    cmpne r0, #0
    beq ov001_0221ed14_L58
    cmp r4, #0
    bne ov001_0221ed14_L50
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #9
    bge ov001_0221ed14_L58
ov001_0221ed14_L50:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov001_0221ed14_L58:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
