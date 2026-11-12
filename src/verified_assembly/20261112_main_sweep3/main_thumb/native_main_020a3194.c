/* main row 0x020a3194: 56 bytes.
 *
 * What it does: calls 1 helper; 1 load, 0 stores; 1 local pool word (0xfffeb007); 6 branches; falls through
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x34 -> constant 0xfffeb007 (image word 0xfffeb007)
 *   branch +0x04 -> +0x0a
 *   branch +0x0c -> +0x18
 *   branch +0x10 -> +0x1c
 *   branch +0x14 -> +0x20
 *   branch +0x16 -> +0x24
 *   branch +0x26 -> +0x2e
 *   test +0x0a cmp r4, #1
 *   test +0x0e cmp r4, #2
 *   test +0x12 cmp r4, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020a3194; the literal pool and
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

extern void native_fn_0209f130(void);


asm u32 native_main_020a3194 (register u32 a0)
{
    push {r4, lr}
    add r4, r0, #0
    bne main_020a3194_La
    mov r0, #0
    pop {r4, pc}
main_020a3194_La:
    cmp r4, #1
    beq main_020a3194_L18
    cmp r4, #2
    beq main_020a3194_L1c
    cmp r4, #3
    beq main_020a3194_L20
    b main_020a3194_L24
main_020a3194_L18:
    mov r0, #1
    pop {r4, pc}
main_020a3194_L1c:
    mov r0, #2
    pop {r4, pc}
main_020a3194_L20:
    mov r0, #3
    pop {r4, pc}
main_020a3194_L24:
    mov r0, #6
    beq main_020a3194_L2e
    ldr r1, =0xfffeb007
    bl native_fn_0209f130
main_020a3194_L2e:
    add r0, r4, #0
    pop {r4, pc}
    mov r8, r8
}
