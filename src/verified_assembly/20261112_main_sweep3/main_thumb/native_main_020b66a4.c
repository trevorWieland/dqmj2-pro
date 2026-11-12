/* main row 0x020b66a4: 60 bytes.
 *
 * What it does: calls 2 helpers; 4 loads, 0 stores; 1 local pool word (0x0100007f); 5 branches, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x38 -> constant 0x0100007f (image word 0x0100007f)
 *   branch +0x0a -> +0x10
 *   branch +0x1a -> +0x34
 *   branch +0x20 -> +0x30
 *   branch +0x2a -> +0x30
 *   back edge +0x32 -> +0x14
 *   test +0x18 cmp r0, #0
 *   test +0x1e cmp r1, r7
 *   test +0x28 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020b66a4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the field meanings and the callee contracts are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020a8dc0(void);
extern void native_fn_020a8e18(void);


asm u32 native_main_020b66a4 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r6, #0
    bl native_fn_020a8dc0
    add r4, r0, #0
    bne main_020b66a4_L10
    add r0, r6, #0
    pop {r3, r4, r5, r6, r7, pc}
main_020b66a4_L10:
    ldr r7, =0x0100007f
    add r5, r6, #0
main_020b66a4_L14:
    ldr r0, [r4, #0xc]
    ldr r0, [r0, r5]
    cmp r0, #0
    beq main_020b66a4_L34
    ldr r1, [r0, #0]
    cmp r1, r7
    beq main_020b66a4_L30
    add r6, r1, #0
    bl native_fn_020a8e18
    cmp r0, #0
    beq main_020b66a4_L30
    add r0, r6, #0
    pop {r3, r4, r5, r6, r7, pc}
main_020b66a4_L30:
    add r5, r5, #4
    b main_020b66a4_L14
main_020b66a4_L34:
    add r0, r6, #0
    pop {r3, r4, r5, r6, r7, pc}
}
