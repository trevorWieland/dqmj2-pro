/* ov001 row 0x02204e24: 188 bytes.
 *
 * What it does: 46 instructions; no calls; no back edge; returns through bx r12; 1 literal slot(s) in the extent
 *
 * Decoded shape: branched body (46 instructions, 0 calls, 28 branches, 0 back edges, 1 literal slot).
 *
 *   pool +0xb8 -> native_fn_02204df0 (image word 0x02204df0)
 *   branch +0x0c -> +0xac
 *   branch +0x10 -> +0xac
 *   branch +0x14 -> +0xa0
 *   branch +0x18 -> +0xa4
 *   branch +0x1c -> +0x78
 *   branch +0x20 -> +0xa8
 *   branch +0x24 -> +0x80
 *   branch +0x28 -> +0x88
 *   branch +0x2c -> +0x58
 *   branch +0x30 -> +0xac
 *   branch +0x34 -> +0x90
 *   branch +0x38 -> +0x94
 *   branch +0x3c -> +0x60
 *   branch +0x40 -> +0x98
 *   branch +0x44 -> +0x68
 *   branch +0x48 -> +0x70
 *   branch +0x4c -> +0x50
 *   branch +0x54 -> +0xac
 *   branch +0x5c -> +0xac
 *   branch +0x64 -> +0xac
 *   branch +0x6c -> +0xac
 *   branch +0x74 -> +0xac
 *   branch +0x7c -> +0xac
 *   branch +0x84 -> +0xac
 *   branch +0x8c -> +0xac
 *   branch +0x94 -> +0xac
 *   branch +0x9c -> +0xac
 *   branch +0xa4 -> +0xac
 *   test +0x00 cmp r1, #15
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204e24; the literal pool and
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

extern void native_fn_02204df0(void);


asm u32 native_ov001_02204e24 (register u32 a0)
{
    cmp r1, #15
    mov r2, #0
    addls pc, pc, r1, lsl #2
    b ov001_02204e24_Lac
    b ov001_02204e24_Lac
    b ov001_02204e24_La0
    b ov001_02204e24_La4
    b ov001_02204e24_L78
    b ov001_02204e24_La8
    b ov001_02204e24_L80
    b ov001_02204e24_L88
    b ov001_02204e24_L58
    b ov001_02204e24_Lac
    b ov001_02204e24_L90
    b ov001_02204e24_L94
    b ov001_02204e24_L60
    b ov001_02204e24_L98
    b ov001_02204e24_L68
    b ov001_02204e24_L70
    b ov001_02204e24_L50
ov001_02204e24_L50:
    mov r2, #12
    b ov001_02204e24_Lac
ov001_02204e24_L58:
    mov r2, #14
    b ov001_02204e24_Lac
ov001_02204e24_L60:
    mov r2, #16
    b ov001_02204e24_Lac
ov001_02204e24_L68:
    mov r2, #13
    b ov001_02204e24_Lac
ov001_02204e24_L70:
    mov r2, #15
    b ov001_02204e24_Lac
ov001_02204e24_L78:
    mov r2, #10
    b ov001_02204e24_Lac
ov001_02204e24_L80:
    mov r2, #4
    b ov001_02204e24_Lac
ov001_02204e24_L88:
    mov r2, #8
    b ov001_02204e24_Lac
ov001_02204e24_L90:
    mov r2, #11
ov001_02204e24_L94:
    b ov001_02204e24_Lac
ov001_02204e24_L98:
    mov r2, #9
    b ov001_02204e24_Lac
ov001_02204e24_La0:
    mov r2, #4
ov001_02204e24_La4:
    b ov001_02204e24_Lac
ov001_02204e24_La8:
    mov r2, #4
ov001_02204e24_Lac:
    ldr r12, =native_fn_02204df0
    mov r1, r2
    bx r12
}
