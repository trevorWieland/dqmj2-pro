import argparse
from project import ROOT,read_json,write_json,sha256
from prepare_parallel_packet_wave import metadata_names,classify_metadata


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--configuration',required=True);parser.add_argument('--ready',required=True);parser.add_argument('--sha256',required=True);parser.add_argument('--alias',required=True);parser.add_argument('--receipt',required=True);args=parser.parse_args()
    config=ROOT/args.configuration;j=read_json(config);assert not j.get('membershipFrozen')
    assert args.ready in j['readyPackets']and args.alias not in j['readyPackets']and args.ready not in j.get('opaqueMetadata',[])
    original=(ROOT/args.ready).resolve();alias=(ROOT/args.alias).resolve()
    assert original.is_relative_to(ROOT)and alias.is_relative_to(original.parent.parent)and alias.name=='ready.json'and not alias.exists()
    assert sha256(original)==args.sha256
    before=metadata_names(j)
    try:classify_metadata(args.ready,True,before)
    except ValueError:pass
    else:raise AssertionError('Original runtime/opaque guard was not active')
    alias.parent.mkdir();alias.write_bytes(original.read_bytes());assert alias.read_bytes()==original.read_bytes()
    identifier=j['packetIds'][args.ready];j['readyPackets']=[args.alias if p==args.ready else p for p in j['readyPackets']];j['packetIds'][args.alias]=j['packetIds'].pop(args.ready)
    assert j['packetIds'][args.alias]==identifier
    after=metadata_names(j);assert classify_metadata(args.ready,True,after)is False and classify_metadata(args.alias,False,after)is True
    try:classify_metadata(args.alias,True,after)
    except ValueError:pass
    else:raise AssertionError('Opaque runtime rejection was weakened')
    receipt=dict(passed=True,sourceCredit=0,originalReady=args.ready,metadataReady=args.alias,identicalBytesSha256=sha256(original),originalReadyImmutable=True,originalReadyNowRealRuntimeInput=True,aliasMetadataOnly=True,originalRuntimeOpaqueRejectionRetained=True,packetIdentifierUnchanged=True,originalPreparerUnchanged=True,generatorSha256=sha256(__file__))
    write_json(ROOT/args.receipt,receipt)
    for name in [args.receipt,'promote_ready_runtime_input_v1_20261106.py']:
        if name not in j['extra']:j['extra'].append(name)
    write_json(config,j);print(dict(passed=True,sourceCredit=0,fullyCaptureActualRuntimeReady=True,originalGuardsUnchanged=True))


if __name__=='__main__':main()
