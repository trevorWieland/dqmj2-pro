import match_overlay_packet95_20261031 as producer
from seal_recovery_sources_20261031 import seal_sources

REPORTS=['evidence/matches/ov001-20261031-gate95.json','evidence/matches/ov006-20261031-dialog95.json']


def main():
    producer.run()
    for report in REPORTS:seal_sources(report,['reproduce_overlay_packet95_20261031.py'])


if __name__=='__main__':main()
