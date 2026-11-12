/* main row 0x02090bdc: 60 bytes.
 *
 * What it does: calls 1 helper; 7 loads, 1 store; 1 local pool word (0x00000818); 3 branches, 1 backward; falls through
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x38 -> constant 0x00000818 (image word 0x00000818)
 *   branch +0x0c -> +0x32
 *   branch +0x20 -> +0x2a
 *   back edge +0x30 -> +0x14
 *   test +0x0a cmp r6, #0
 *   test +0x1e cmp r0, #0
 *   test +0x2e cmp r4, r6
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02090bdc; the literal pool and
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

extern void native_fn_0201d800(void);


asm u32 native_main_02090bdc (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r7, r1, #0
    ldr r1, =0x00000818
    mov r4, #0
    ldr r6, [r0, r1]
    cmp r6, #0
    ble main_02090bdc_L32
    sub r1, r1, #4
    ldr r5, [r0, r1]
    str r5, [sp]
main_02090bdc_L14:
    ldr r0, [r5, #0]
    add r1, r7, #0
    ldr r0, [r0, #0]
    blx native_fn_0201d800
    cmp r0, #0
    bne main_02090bdc_L2a
    ldr r0, [sp]
    lsl r1, r4, #2
    ldr r0, [r0, r1]
    pop {r3, r4, r5, r6, r7, pc}
main_02090bdc_L2a:
    add r4, r4, #1
    add r5, r5, #4
    cmp r4, r6
    blt main_02090bdc_L14
main_02090bdc_L32:
    mov r0, #0
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
