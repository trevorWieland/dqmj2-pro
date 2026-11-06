import stat
from pathlib import Path
from project import sha256,read_json


class LookupEpochChanged(ValueError):pass


class PathLookupEpoch:
    def __init__(self,root):
        self.root=Path(root);self.resolutions={};self.files={};self.directories={};self.hashes={};self.observedChange=False;self.counts=dict(resolveCalls=0,resolveHits=0,isFileCalls=0,isFileHits=0,contentHashCalls=0)
        for name in ['recovery.json','source-preferences.json','interpreted-recovery.json']:
            path=self.root/name;self.resolve(path)
            if self.is_file(path):self.hash(path)
    def fail(self,reason):self.observedChange=True;raise LookupEpochChanged(reason)
    def kind(self,path):
        try:
            value=Path(path).stat();return ('stat',stat.S_IFMT(value.st_mode),value.st_dev,value.st_ino)
        except (OSError,ValueError) as error:return ('error',type(error).__name__,getattr(error,'errno',None),getattr(error,'winerror',None))
    def directory(self,path):
        path=Path(path);key=str(path)
        if key not in self.directories:self.directories[key]=(path,self.kind(path))
    def resolve(self,path):
        self.counts['resolveCalls']+=1;path=Path(path);key=str(path)
        if key in self.resolutions:self.counts['resolveHits']+=1;return self.resolutions[key][1]
        try:value=path.resolve()
        except (OSError,ValueError):self.observedChange=True;raise
        self.resolutions[key]=(path,value);self.directory(path.parent);self.directory(value.parent);return value
    def is_file(self,path):
        self.counts['isFileCalls']+=1;path=Path(path);key=str(path)
        if key in self.files:self.counts['isFileHits']+=1;return self.files[key][1]
        value=path.is_file();kind=self.kind(path)
        if value!=(kind[0]=='stat' and kind[1]==stat.S_IFREG):self.fail('File lookup changed while its type fact was recorded')
        self.files[key]=(path,value,kind);self.directory(path.parent);return value
    def hash(self,path):
        self.counts['contentHashCalls']+=1;path=Path(path);key=str(path)
        try:digest=sha256(path)
        except (OSError,ValueError):self.observedChange=True;raise
        if key in self.hashes and self.hashes[key][1]!=digest:self.fail('Observed collector input content changed')
        self.hashes[key]=(path,digest);return digest
    def read_json(self,path):
        self.hash(path)
        try:return read_json(path)
        finally:self.hash(path)
    def verify(self):
        if self.observedChange:self.fail('A collector epoch change was already observed, even if restored')
        for path,target in self.resolutions.values():
            try:actual=path.resolve()
            except (OSError,ValueError):self.fail('A queried path resolution is no longer readable')
            if str(actual)!=str(target):self.fail('A queried path resolution target changed')
        for path,value,kind in self.files.values():
            if path.is_file()!=value or self.kind(path)!=kind:self.fail('A queried file/missing/type/identity fact changed')
        for path,kind in self.directories.values():
            if self.kind(path)!=kind:self.fail('A queried parent directory type/identity fact changed')
        for path,digest in self.hashes.values():
            try:actual=sha256(path)
            except (OSError,ValueError):self.fail('A captured collector input is no longer readable')
            if actual!=digest:self.fail('A captured collector input content hash changed')
    def summary(self):return dict(self.counts,uniqueResolutions=len(self.resolutions),uniqueFileTypeFacts=len(self.files),recordedNonFiles=sum(not row[1] for row in self.files.values()),recordedMissingFacts=sum(row[2][0]=='error' for row in self.files.values()),directoryFacts=len(self.directories),contentFacts=len(self.hashes),observedChange=self.observedChange)
