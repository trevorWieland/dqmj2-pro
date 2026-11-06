import match_ov006_transition130_20261031 as producer
from seal_recovery_sources_20261031 import seal_sources

REPORTS=['evidence/matches/ov006-20261031-transition130.json','evidence/matches/ov006-20261031-predicate130.json']


def main():
    producer.run()
    for report in REPORTS:seal_sources(report,['reproduce_ov006_transition130_20261031.py'])


if __name__=='__main__':main()
