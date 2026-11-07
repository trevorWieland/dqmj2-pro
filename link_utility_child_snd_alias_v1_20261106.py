import argparse
from utility_child_snd_alias_v1_20261106 import factory
from build_lock import accepted_build
import link_utility


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean', action='store_true')
    args = parser.parse_args()
    with accepted_build():
        with factory(link_utility):
            link_utility.main(args.clean)


if __name__ == '__main__':
    main()
