/* ov000 row 0x0221fbb8: 180 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (one load, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xa8 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0xac -> constant 0x022463f6 (image word 0x022463f6)
 *   pool +0xb0 -> constant 0x021c9698 (image word 0x021c9698)
 *   back edge +0x8c -> +0x80
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221fbb8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0221f6e8(void);
extern void native_fn_0207cd98(void);
extern void native_fn_02062a10(void);
extern void native_fn_02046af4(void);
extern void native_fn_0221cab0(void);


asm u32 native_ov000_0221fbb8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #8
    ldr r1, =0x022463b0
    ldr r0, [r0]
    ldr r1, [r1, #0xc]
    and r1, r1, #255
    bl native_fn_0221f6e8
    mov r5, r0
    bl native_fn_0207cd98
    bl native_fn_02062a10
    mov r4, r0
    mov r0, r5
    bl native_fn_0207cd98
    bl native_fn_02062a10
    ldr r2, =0x022463b0
    mov r1, r0
    ldr r3, [r2, #0xc]
    ldr r12, =0x022463f6
    mov r0, #20
    mla r0, r3, r0, r12
    mov r2, #255
    stmia sp, {r0, r2}
    ldr r0, =0x021c9698
    mov r2, #18
    mov r3, #24
    bl native_fn_02046af4
    ldr r1, =0x022463b0
    mov r0, #132
    ldr r2, [r1, #0x1c]
    ldr r1, [r1, #0xc]
    mov r12, #8
    mla r14, r1, r0, r2
ov000_0221fbb8_L80:
    ldmia r4!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    subs r12, r12, #1
    bne ov000_0221fbb8_L80
    ldr r0, [r4]
    str r0, [lr]
    bl native_fn_0221cab0
    mov r0, #1
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
}
