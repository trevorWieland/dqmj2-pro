/* ov006 row 0x02200730: 64 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x38 -> native_data_0221c15c (image word 0x0221c15c)
 *   pool +0x3c -> native_fn_02200950+1 (image word 0x02200951)
 *   branch +0x1c -> +0x36
 *   test +0x1a cmp r0, #0x78
 *   3 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200730; the literal pool and
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

extern u8 native_data2_0221c15c[];
extern void native_fn_02204974(void);
extern void native_fn_02200950(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_02200730 (register u32 a0)
{
    push {r3, lr}
    add r1, r0, #0x0
    ldr r0, =native_data2_0221c15c
    mov r3, #0x0
    ldr r2, [r0, #0]
    mvn r3, r3
    strb r3, [r2, #0x1b]
    ldr r3, [r0, #0]
    ldrh r2, [r3, #0x18]
    add r2, r2, #0x1
    strh r2, [r3, #0x18]
    ldr r0, [r0, #0]
    ldrh r0, [r0, #0x18]
    cmp r0, #0x78
    blo ov006_02200730_L36
    mov r0, #0x0
    bl native_fn_02204974
    ldr r1, =native_fn_02200950+1
    mov r0, #0x1
    mov r2, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =native_data2_0221c15c
    ldr r1, [r1, #0]
    str r0, [r1, #0x14]
ov006_02200730_L36:
    pop {r3, pc}
}
