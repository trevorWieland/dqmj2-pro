/* ov001 row 0x02212fb0: 152 bytes.
 *
 * What it does: 36 instructions; 6 call(s) to 0x022135d4, 0x02212f14, 0x021f949c, +3 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (36 instructions, 6 calls, 5 branches, 5 back edges, 2 literal slots).
 *
 *   pool +0x90 -> constant 0x00000106 (image word 0x00000106)
 *   pool +0x94 -> constant 0x00000119 (image word 0x00000119)
 *   branch +0x18 -> +0x64
 *   branch +0x34 -> +0x44
 *   branch +0x40 -> +0x4c
 *   branch +0x60 -> +0x88
 *   branch +0x70 -> +0x88
 *   test +0x14 cmp r0, #0
 *   test +0x30 cmp r0, #1000
 *   test +0x6c cmp r1, r0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02212fb0; the literal pool and
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

extern void native_fn_022135d4(void);
extern void native_fn_02212f14(void);
extern void native_fn_021f949c(void);
extern void native_fn_02212b68(void);


asm u32 native_ov001_02212fb0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldr r5, [r6, #0x40]
    mov r4, #0
    bl native_fn_022135d4
    cmp r0, #0
    beq ov001_02212fb0_L64
    mov r0, r6
    mov r1, #2
    bl native_fn_02212f14
    ldr r0, [r6, #0x30]
    mov r1, #1
    cmp r0, #1000
    bge ov001_02212fb0_L44
    mov r0, #96
    bl native_fn_021f949c
    b ov001_02212fb0_L4c
ov001_02212fb0_L44:
    ldr r0, =0x00000106
    bl native_fn_021f949c
ov001_02212fb0_L4c:
    ldr r1, [r6, #0x30]
    mov r0, r6
    str r1, [r5, #0x20]
    bl native_fn_02212b68
    mov r4, #1
    b ov001_02212fb0_L88
ov001_02212fb0_L64:
    ldr r1, [r5, #0x20]
    ldr r0, [r6, #0x30]
    cmp r1, r0
    beq ov001_02212fb0_L88
    ldr r0, =0x00000119
    mov r1, #1
    bl native_fn_021f949c
    ldr r0, [r6, #0x30]
    str r0, [r5, #0x20]
ov001_02212fb0_L88:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
}
