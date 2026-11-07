import subprocess

def staged_names(index_bytes, tree_bytes):
    index, tree = {}, {}
    for record in index_bytes.split(b'\0'):
        if not record:
            continue
        header, path = record.split(b'\t',1)
        mode, digest, stage = header.split()
        if stage != b'0' or path in index:
            raise ValueError('Unmerged or duplicate index entry')
        index[path] = mode,digest
    for record in tree_bytes.split(b'\0'):
        if not record:
            continue
        header,path = record.split(b'\t',1)
        mode,kind,digest = header.split()
        if path in tree:
            raise ValueError('Duplicate HEAD tree entry')
        tree[path] = mode,digest
    return sorted(path.decode('utf-8') for path in index.keys() | tree.keys() if index.get(path) != tree.get(path))

def names(process, root):
    index = process.check_output(['git','ls-files','--stage','-z'],cwd=root)
    tree = process.check_output(['git','ls-tree','-r','--full-tree','HEAD','-z'],cwd=root)
    return staged_names(index,tree)

def check(process,root,command,paths):
    stdout,stderr,codes = [],[],[]
    batch,length = [],0
    batches = []
    for name in paths:
        if batch and length + len(name) + 3 > 16000:
            batches.append(batch)
            batch,length = [],0
        if len(name) + 3 > 16000:
            raise ValueError('Staged filename exceeds checked Windows argv budget')
        batch.append(name)
        length += len(name)+3
    if batch:
        batches.append(batch)
    for batch in batches:
        result = process.run([*command,'--',*batch],cwd=root,capture_output=True,text=True,encoding='utf-8')
        codes.append(result.returncode)
        stdout.append(result.stdout)
        stderr.append(result.stderr)
    return subprocess.CompletedProcess(command,max(codes,default=0),''.join(stdout),''.join(stderr))
