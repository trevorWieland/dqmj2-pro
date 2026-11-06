import match_overlay_counter103_20261031 as producer
from seal_recovery_sources_20261031 import seal_sources

REPORTS=['evidence/matches/ov001-20261031-statea103.json','evidence/matches/ov001-20261031-stateb103.json']


def main():
    producer.run()
    for report in REPORTS:seal_sources(report,['reproduce_overlay_counter103_20261031.py'])


if __name__=='__main__':main()
