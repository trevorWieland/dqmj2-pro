/* ov001 row 0x021ff2a8: 168 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x98 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x9c -> constant 0x02239e7c (image word 0x02239e7c)
 *   pool +0xa0 -> native_fn_021ff094 (image word 0x021ff094)
 *   pool +0xa4 -> native_fn_021ff1f8 (image word 0x021ff1f8)
 *   branch +0x14 -> +0x8c
 *   back edge +0x68 -> +0x5c
 *   test +0x10 cmp r1, #0
 *   7 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ff2a8; the literal pool and
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

extern void native_fn_021ff094(void);
extern void native_fn_021ff1f8(void);
extern void native_fn_0205fc10(void);
extern void native_fn_0205fd0c(void);
extern void native_fn_02203098(void);


asm u32 native_ov001_021ff2a8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    ldr r0, =0x02239c10
    ldrb r1, [r0, #0x2]
    cmp r1, #0
    beq ov001_021ff2a8_L8c
    mov r3, #0
    strb r3, [r0, #0xf]
    mov r0, #18
    str r0, [sp]
    mov r0, #8192
    str r0, [sp, #0x4]
    mov r4, #2
    str r4, [sp, #0x8]
    mov r4, #1
    ldr r0, =0x02239e7c
    ldr r1, =native_fn_021ff094
    ldr r2, =native_fn_021ff1f8
    str r4, [sp, #0xc]
    bl native_fn_0205fc10
    ldr lr, =0x02239e7c
    mov r4, r0
    mov r12, #13
ov001_021ff2a8_L5c:
    ldmia r4!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    subs r12, r12, #1
    bne ov001_021ff2a8_L5c
    ldr r0, =0x02239e7c
    bl native_fn_0205fd0c
    bl native_fn_02203098
    ldr r0, =0x02239c10
    mov r1, #1
    strb r1, [r0, #0xa]
    mov r1, #0
    strb r1, [r0]
ov001_021ff2a8_L8c:
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
