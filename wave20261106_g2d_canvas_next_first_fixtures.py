import hashlib,random,struct
import match_runtime
from project import ROOT
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,DATA,STACK,STOP=0x2000000,0x2300000,0x3000000,0x4000000
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC]
SPANS={0x2087fa8:576,0x20881e8:408,0x2034ab8:96}

def cases(address):
 return list(range(20))if address==0x2087fa8 else list(range(22))

def pixel(page,start,position,bpp):
 value=0
 for k in range(bpp):value=value*2+((page[start+(position+k)//8]>>(7-(position+k)%8))&1)
 return value

def put(page,offset,shift,bpp,value):
 mask=((1<<bpp)-1)<<shift;page[offset]=(page[offset]&~mask)|(value<<shift)

def prepare(address,index):
 rng=random.Random(address+index);page=bytearray(rng.randbytes(16384));dst_bpp=[4,8][index%2];src_bpp=min([1,2,4,8][index//2%4],dst_bpp);cl=rng.randrange((1<<dst_bpp)-(1<<src_bpp)+1)
 x,y=[(-7,-7),(0,0),(3,7),(7,3),(8,0),(0,8),(-17,0),(24,0),(0,-17),(0,24),(2,2)][index//2%11];width=12 if index!=18 else 0;height=13;glyph=0x1000;tile=0x2000
 if index in[16,17]:page[glyph:glyph+2048]=bytes(2048)
 expected=bytearray(page);writes=0
 if address==0x2087fa8:
  if x+width<0:x=-width
  if y+height<0:y=-height
  stride=width*src_bpp+3;struct.pack_into('<II7iI',page,0x400,DATA+tile,DATA+glyph,x,y,width,height,stride,src_bpp,dst_bpp,cl);expected=bytearray(page)
  for dy in range(max(0,y),min(8,y+height)):
   for dx in range(max(0,x),min(8,x+width)):
    value=pixel(page,glyph,(dy-y)*stride+(dx-x)*src_bpp,src_bpp)
    if value:put(expected,tile+dy*dst_bpp+dx*dst_bpp//8,dx*dst_bpp%8,dst_bpp,cl+value);writes+=1
  args=[DATA+0x400];context=dict(sourceStrideBits=stride,canvasTiles=[1,1])
 else:
  cell_width=16;stride=cell_width*src_bpp;area_width,area_height,line_stride=2+(index%3==0),2,4
  struct.pack_into('<III B3x II',page,0x400,DATA+tile,area_width,area_height,dst_bpp,line_stride,0);struct.pack_into('<II',page,0x500,DATA+0x600,0);struct.pack_into('<I',page,0x608,DATA+0x700);struct.pack_into('<BBHbbBB',page,0x700,cell_width,height,128,0,width,src_bpp,0);struct.pack_into('<II',page,0x800,DATA+0x900,DATA+glyph);struct.pack_into('<bBb',page,0x900,-2,width,13);expected=bytearray(page)
  for sy in range(height):
   for sx in range(width):
    dx,dy=x+sx,y+sy
    if 0<=dx<area_width*8 and 0<=dy<area_height*8:
     value=pixel(page,glyph,sy*stride+sx*src_bpp,src_bpp)
     if value:
      offset=tile+((dy//8)*line_stride+dx//8)*8*dst_bpp+(dy%8)*dst_bpp+(dx%8)*dst_bpp//8;put(expected,offset,(dx%8)*dst_bpp%8,dst_bpp,cl+value);writes+=1
  args=[DATA+0x400,DATA+0x500,x,y,cl+1,DATA+0x800];context=dict(sourceCellWidth=cell_width,canvasTiles=[area_width,area_height],lineStrideTiles=line_stride)
 context.update(dstBpp=dst_bpp,srcBpp=src_bpp,x=x,y=y,width=width,height=height,colorBase=cl,nontransparentPixels=writes,validPaletteSum=True,transparentSource=index in[16,17]);return page,bytes(expected),args,context

def run(address,bodies,index,bound=250000):
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes();page,expected,args,context=prepare(address,index);rng=random.Random(0x946+address+index);machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946);machine.mem_map(BASE,0x200000);machine.mem_write(BASE,image)
 for at,body in bodies.items():machine.mem_write(at,body)
 machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,16384);machine.mem_write(STACK,rng.randbytes(16384));machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xf0000000]))
 for r in REGS:machine.reg_write(r,rng.getrandbits(32))
 for r,v in zip(REGS[:4],args):machine.reg_write(r,v&0xffffffff)
 sp=STACK+8192
 for i,v in enumerate(args[4:]):machine.mem_write(sp+4*i,struct.pack('<I',v&0xffffffff))
 machine.reg_write(UC_ARM_REG_SP,sp);machine.reg_write(UC_ARM_REG_LR,STOP);seen=set();reads=[];writes=[];providers=[];pending=[];returned=False
 def code(uc,pc,size,user):
  nonlocal returned
  if pending and pc==pending[-1][0]:pending.pop()
  if pc==STOP:assert not pending;returned=True;uc.emu_stop();return
  assert any(a<=pc<a+n for a,n in SPANS.items()),hex(pc);seen.add(pc)
  if pc!=address and pc in SPANS:
   providers.append(dict(entry=hex(pc),args=[uc.reg_read(r)for r in REGS[:4]]));pending.append((uc.reg_read(UC_ARM_REG_LR),pc))
 def read(uc,access,at,size,value,user):reads.append((at,size,int.from_bytes(bytes(uc.mem_read(at,size)),'little')))
 def write(uc,access,at,size,value,user):
  assert DATA<=at and at+size<=DATA+16384 or STACK<=at and at+size<=STACK+16384
  writes.append((at,size,value))
 machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write);machine.emu_start(address,STOP+4,count=bound);assert returned,('not returned',hex(address),index);assert machine.reg_read(UC_ARM_REG_SP)==sp
 output=bytes(machine.mem_read(DATA,16384))
 for at,body in bodies.items():machine.mem_write(at,image[at-BASE:at-BASE+len(body)])
 assert bytes(machine.mem_read(BASE,len(image)))==image
 return dict(address=hex(address),index=index,context=context,actualReturn=True,modelPassed=output==expected,registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,providers=providers,dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,16384))).hexdigest(),ownObserved=sorted(seen),providerSourceOrExecutionCredit=0)

def compare(bodies):
 result=[]
 for address in bodies:
  for index in cases(address):
   native=run(address,{},index);source=run(address,bodies,index);assert native['modelPassed']and source['modelPassed'],('pixel model',hex(address),index,native['modelPassed'],source['modelPassed'])
   assert native==source,('native/source state',hex(address),index);result.append(native)
 return dict(allPassed=True,cases=result,caseCount=len(result),actualNativeAndSourceReturns=2*len(result),independentClippedPixelAndTiledCanvasModel=True,providerSourceOrExecutionCredit=0,limits=['Bounded valid glyph/canvas/source backing domains; source BPP <= destination BPP and palette addition fits.','Imported original 96-byte bit-reader executes with zero new credit; selected draw-line source invokes newly linked selected LetterChar.','No GPU, font-resource parser, game scene or platform execution claim.'])
