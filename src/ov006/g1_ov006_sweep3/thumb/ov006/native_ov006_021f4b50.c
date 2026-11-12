/* ov006 row 0x021f4b50: 96 bytes.
 *
 * What it does: 38 instructions; 4 call(s) to 0x02202dc0, 0x02202ff0, 0x02202f54, +1 more; no back edge; returns through pop {r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x54 -> constant 0x0221c060 (image word 0x0221c060)
 *   pool +0x58 -> native_data_0220b4ac (image word 0x0220b4ac)
 *   pool +0x5c -> native_data_0220b4aa (image word 0x0220b4aa)
 *   branch +0x0c -> +0x12
 *   branch +0x10 -> +0x14
 *   test +0x0a cmp r0, #0xb
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4b50; the literal pool and
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

extern void native_fn_02202dc0(void);
extern void native_fn_02202ff0(void);
extern void native_fn_02202f54(void);
extern u8 native_data_0220b4ac[];
extern u8 native_data_0220b4aa[];
extern void native_fn_02202eb0(void);


asm u32 native_ov006_021f4b50 (register u32 a0)
{
    push {r4, lr}
    ldr r0, =0x0221c060
    ldr r1, [r0, #0]
    mov r0, #0x63
    ldrsb r0, [r1, r0]
    cmp r0, #0xb
    bgt ov006_021f4b50_L12
    mov r4, #0x44
    b ov006_021f4b50_L14
ov006_021f4b50_L12:
    mov r4, #0x45
ov006_021f4b50_L14:
    ldr r0, [r1, #0x58]
    mov r1, #0x0
    bl native_fn_02202dc0
    add r2, r0, #0x0
    mov r0, #0x0
    add r1, r4, #0x0
    bl native_fn_02202ff0
    ldr r0, =0x0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    ldr r0, [r0, #0x58]
    mov r2, #0x2
    bl native_fn_02202f54
    ldr r0, =0x0221c060
    mov r1, #0x63
    ldr r2, [r0, #0]
    ldr r3, =native_data_0220b4ac
    ldrsb r0, [r2, r1]
    sub r1, #0x64
    lsl r4, r0, #0x2
    ldr r0, [r2, #0x58]
    ldr r2, =native_data_0220b4aa
    ldrh r3, [r3, r4]
    ldrh r2, [r2, r4]
    bl native_fn_02202eb0
    pop {r4, pc}
    mov r8, r8
}
